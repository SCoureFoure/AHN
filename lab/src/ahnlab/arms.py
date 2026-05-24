"""R5 Arm Controller — execute an ExperimentSpec across arms with resume support."""
from __future__ import annotations

import json
from pathlib import Path

from anthropic import Anthropic
from rich.console import Console

from .config import ANTHROPIC_API_KEY, RUNS_DIR
from .harness import run_task
from .membrane import run_suite
from .models import ExperimentSpec, TaskSpec
from .store import Store


console = Console()


def execute(
    spec: ExperimentSpec,
    subjects_root: Path,
    hidden_root: Path,
    store: Store,
) -> None:
    """Run every (arm, subject, seed) trial that hasn't completed yet.

    Resume semantics: skip a trial if a run already exists with matching
    (experiment_id, arm_id, subject, seed).
    """
    store.upsert_experiment(spec.experiment_id, spec.description, spec.model_dump_json())
    for arm in spec.arms:
        store.upsert_arm(spec.experiment_id, arm.arm_id, arm.description, arm.include_contracts)

    client = Anthropic(api_key=ANTHROPIC_API_KEY)
    manifest_path = RUNS_DIR / spec.experiment_id / "manifest.jsonl"
    manifest_path.parent.mkdir(parents=True, exist_ok=True)

    for subject in spec.subjects:
        subject_dir = subjects_root / subject
        intent_path = subject_dir / "intent.md"
        contract_files = sorted(subject_dir.glob("contracts*.py"))
        hidden_files = sorted(hidden_root.glob(f"{subject}_hidden*.py"))
        if not intent_path.exists():
            console.print(f"[yellow]skip subject {subject}: missing intent.md[/]")
            continue
        intent_text = intent_path.read_text(encoding="utf-8")

        for arm in spec.arms:
            # Resolve contract files for this arm: explicit list takes priority over glob.
            if arm.include_contracts:
                if arm.contract_filenames:
                    arm_contract_files = [subject_dir / fn for fn in arm.contract_filenames]
                else:
                    arm_contract_files = contract_files
            else:
                arm_contract_files = []

            existing = {(r["run_id"]) for r in store.runs_for(spec.experiment_id, arm.arm_id, subject)}
            done_count = len(existing)
            for seed in spec.seed_schedule[:spec.trials_per_arm]:
                # Resume by counting; simple v1.
                # (Future: persist seed→run_id map for exact resume.)
                if done_count > 0:
                    done_count -= 1
                    continue

                spec_task = TaskSpec(
                    task_id=f"{spec.experiment_id}:{subject}:{arm.arm_id}:{seed}",
                    subject=subject,
                    intent_text=intent_text,
                    model=spec.model,
                    contract_files=arm_contract_files,
                )
                console.print(f"[cyan]run[/] exp={spec.experiment_id} arm={arm.arm_id} subj={subject} seed={seed}")
                try:
                    rec = run_task(
                        spec_task, spec.experiment_id, arm.arm_id, seed,
                        include_contracts=arm.include_contracts, client=client,
                    )
                except Exception as e:  # noqa: BLE001 — arm controller must isolate per-trial failures
                    console.print(f"[red]harness error[/] {type(e).__name__}: {e}")
                    continue

                store.insert_run(rec)
                with manifest_path.open("a", encoding="utf-8") as mf:
                    mf.write(json.dumps({
                        "run_id": rec.run_id, "experiment_id": rec.experiment_id,
                        "arm_id": rec.arm_id, "subject": rec.subject, "seed": rec.seed,
                        "terminal_status": rec.terminal_status,
                    }) + "\n")

                # Score with hidden suite (always) and contract suite (always — useful for both arms).
                if hidden_files:
                    try:
                        hidden_report = run_suite(rec.run_id, rec.artifacts_dir, hidden_files, "hidden")
                        store.insert_membrane_report(hidden_report)
                        console.print(
                            f"  hidden: {hidden_report.passed}/{hidden_report.total} passed"
                        )
                    except Exception as e:  # noqa: BLE001
                        console.print(f"[red]hidden suite error[/] {e}")
                if contract_files:
                    try:
                        contract_report = run_suite(rec.run_id, rec.artifacts_dir, contract_files, "contracts")
                        store.insert_membrane_report(contract_report)
                    except Exception as e:  # noqa: BLE001
                        console.print(f"[red]contract suite error[/] {e}")
