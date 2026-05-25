"""Multi-cycle experiment runner — chains N sequential agent calls per trial."""
from __future__ import annotations

import uuid
from pathlib import Path

from anthropic import Anthropic
from rich.console import Console

from .config import ANTHROPIC_API_KEY
from .harness import run_cycle, run_multi_file_cycle
from .membrane import run_suite
from .models import MultiCycleExperimentSpec, MultiFileExperimentSpec
from .store import Store


console = Console()


def execute_cycles(
    spec: MultiCycleExperimentSpec,
    subjects_root: Path,
    store: Store,
) -> None:
    store.upsert_experiment(spec.experiment_id, spec.description, spec.model_dump_json())
    for arm in spec.arms:
        store.upsert_arm(spec.experiment_id, arm.arm_id, arm.description, arm.include_contracts)

    client = Anthropic(api_key=ANTHROPIC_API_KEY)

    for arm in spec.arms:
        completed_chains = store.count_chains(spec.experiment_id, arm.arm_id, spec.subject)
        for trial_idx in range(spec.trials_per_arm):
            if trial_idx < completed_chains:
                continue

            seed = spec.seed_schedule[trial_idx]
            chain_id = uuid.uuid4().hex[:12]
            prior_code: str | None = None

            for cycle in spec.cycles:
                seed_code = cycle.seed_path.read_text(encoding="utf-8") if prior_code is None else prior_code
                contract_files = [cycle.contract_path] if (arm.include_contracts and cycle.contract_path) else []

                console.print(
                    f"[cyan]cycle[/] exp={spec.experiment_id} arm={arm.arm_id} "
                    f"seed={seed} c{cycle.cycle_num}"
                )
                try:
                    rec = run_cycle(
                        intent_text=cycle.intent_path.read_text(encoding="utf-8"),
                        prior_code=seed_code,
                        contract_files=contract_files,
                        include_contracts=arm.include_contracts,
                        experiment_id=spec.experiment_id,
                        arm_id=arm.arm_id,
                        subject=spec.subject,
                        seed=seed,
                        cycle_num=cycle.cycle_num,
                        chain_id=chain_id,
                        model=spec.model,
                        client=client,
                    )
                except Exception as e:  # noqa: BLE001
                    console.print(f"[red]cycle error[/] {type(e).__name__}: {e}")
                    break

                store.insert_run(rec)

                solution_path = rec.artifacts_dir / "solution.py"
                if solution_path.exists():
                    prior_code = solution_path.read_text(encoding="utf-8")
                else:
                    console.print(f"[yellow]  no solution.py — chain broken at c{cycle.cycle_num}[/]")
                    break

                if cycle.hidden_paths:
                    try:
                        report = run_suite(rec.run_id, rec.artifacts_dir, cycle.hidden_paths, "hidden")
                        store.insert_membrane_report(report)
                        console.print(f"  hidden_c{cycle.cycle_num}: {report.passed}/{report.total} passed")
                    except Exception as e:  # noqa: BLE001
                        console.print(f"[red]  hidden suite error[/] {e}")


def execute_multi_file_cycles(
    spec: MultiFileExperimentSpec,
    subjects_root: Path,
    store: Store,
) -> None:
    store.upsert_experiment(spec.experiment_id, spec.description, spec.model_dump_json())
    for arm in spec.arms:
        store.upsert_arm(spec.experiment_id, arm.arm_id, arm.description, arm.include_contracts)

    client = Anthropic(api_key=ANTHROPIC_API_KEY)

    for arm in spec.arms:
        completed_chains = store.count_chains(spec.experiment_id, arm.arm_id, spec.subject)
        for trial_idx in range(spec.trials_per_arm):
            if trial_idx < completed_chains:
                continue

            seed = spec.seed_schedule[trial_idx]
            chain_id = uuid.uuid4().hex[:12]
            prior_files: dict[str, str] | None = None

            for cycle in spec.cycles:
                if prior_files is None:
                    prior_files = {
                        p.name: p.read_text(encoding="utf-8")
                        for p in sorted(cycle.seed_dir.glob("*.py"))
                    }

                contract_files = [cycle.contract_path] if (arm.include_contracts and cycle.contract_path) else []

                console.print(
                    f"[cyan]cycle[/] exp={spec.experiment_id} arm={arm.arm_id} "
                    f"seed={seed} c{cycle.cycle_num}"
                )
                try:
                    rec = run_multi_file_cycle(
                        intent_text=cycle.intent_path.read_text(encoding="utf-8"),
                        prior_files=prior_files,
                        contract_files=contract_files,
                        include_contracts=arm.include_contracts,
                        experiment_id=spec.experiment_id,
                        arm_id=arm.arm_id,
                        subject=spec.subject,
                        seed=seed,
                        cycle_num=cycle.cycle_num,
                        chain_id=chain_id,
                        model=spec.model,
                        client=client,
                    )
                except Exception as e:  # noqa: BLE001
                    console.print(f"[red]cycle error[/] {type(e).__name__}: {e}")
                    break

                store.insert_run(rec)

                artifact_files = {
                    p.name: p.read_text(encoding="utf-8")
                    for p in sorted(rec.artifacts_dir.glob("*.py"))
                    if p.name != "__init__.py"
                }
                if not artifact_files:
                    console.print(f"[yellow]  no .py files — chain broken at c{cycle.cycle_num}[/]")
                    break

                # merge: keep prior files, overlay with agent's updates
                prior_files = {**prior_files, **artifact_files}

                # ensure artifacts dir has ALL files (agent may only emit changed files)
                for fname, content in prior_files.items():
                    dest = rec.artifacts_dir / fname
                    if not dest.exists():
                        dest.write_text(content, encoding="utf-8")

                if cycle.hidden_paths:
                    try:
                        report = run_suite(rec.run_id, rec.artifacts_dir, cycle.hidden_paths, "hidden")
                        store.insert_membrane_report(report)
                        console.print(f"  hidden_c{cycle.cycle_num}: {report.passed}/{report.total} passed")
                    except Exception as e:  # noqa: BLE001
                        console.print(f"[red]  hidden suite error[/] {e}")
