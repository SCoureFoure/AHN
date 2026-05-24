"""Diagnostic: slugify arms A+B at temperature=0, N=10 trials.

Answers: does A_control divergence collapse to 0.000 at temp=0?
If yes: E1 slugify convergence was sampling noise, not interpretation convergence.
Stored as experiment_id='E1-DIAG-T0' to avoid contaminating E1 results.
"""
from __future__ import annotations

import sys
from pathlib import Path

# Make lab src importable
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from anthropic import Anthropic
from rich.console import Console
from rich.table import Table

from ahnlab.config import ANTHROPIC_API_KEY, RUNS_DIR, ensure_dirs
from ahnlab.harness import run_task
from ahnlab.membrane import run_suite
from ahnlab.metrics import mean_pairwise_hamming, pass_rate
from ahnlab.models import ArmSpec, TaskSpec
from ahnlab.store import Store

EXPERIMENT_ID = "E1-DIAG-T0"
SUBJECT = "slugify"
TEMPERATURE = 0.0
N_TRIALS = 10
MODEL = "claude-haiku-4-5-20251001"
SEEDS = list(range(101, 101 + N_TRIALS))  # distinct from E1 seeds (1-30)

SUBJECTS_ROOT = Path(__file__).resolve().parents[1] / "experiments" / "E1" / "subjects"
HIDDEN_ROOT = Path(__file__).resolve().parents[1] / "experiments" / "E1" / "hidden"

ARMS = [
    ArmSpec(arm_id="A_control", description="Intent only, no contracts.", include_contracts=False),
    ArmSpec(arm_id="B_contracts", description="Intent + failing acceptance tests.", include_contracts=True),
]

console = Console()


def run_diag() -> None:
    if not ANTHROPIC_API_KEY:
        console.print("[red]ANTHROPIC_API_KEY missing[/]")
        sys.exit(2)

    ensure_dirs()
    store = Store()
    store.upsert_experiment(EXPERIMENT_ID, f"Temperature=0 pilot: slugify A+B N={N_TRIALS}", "{}")
    for arm in ARMS:
        store.upsert_arm(EXPERIMENT_ID, arm.arm_id, arm.description, arm.include_contracts)

    subject_dir = SUBJECTS_ROOT / SUBJECT
    intent_text = (subject_dir / "intent.md").read_text(encoding="utf-8")
    contract_files = sorted(subject_dir.glob("contracts*.py"))
    hidden_files = sorted(HIDDEN_ROOT.glob(f"{SUBJECT}_hidden*.py"))

    client = Anthropic(api_key=ANTHROPIC_API_KEY)

    for arm in ARMS:
        existing_count = store.count_runs(EXPERIMENT_ID, arm.arm_id, SUBJECT)
        skip = existing_count
        for seed in SEEDS:
            if skip > 0:
                skip -= 1
                console.print(f"[dim]skip (resume)[/] arm={arm.arm_id} seed={seed}")
                continue
            console.print(f"[cyan]run[/] arm={arm.arm_id} seed={seed} temp={TEMPERATURE}")
            task = TaskSpec(
                task_id=f"{EXPERIMENT_ID}:{SUBJECT}:{arm.arm_id}:{seed}",
                subject=SUBJECT,
                intent_text=intent_text,
                model=MODEL,
                temperature=TEMPERATURE,
                contract_files=contract_files if arm.include_contracts else [],
            )
            try:
                rec = run_task(task, EXPERIMENT_ID, arm.arm_id, seed,
                               include_contracts=arm.include_contracts, client=client)
            except Exception as e:
                console.print(f"[red]error[/] {e}")
                continue
            store.insert_run(rec)
            if hidden_files and rec.terminal_status == "ok":
                hidden_report = run_suite(rec.run_id, rec.artifacts_dir, hidden_files, "hidden")
                store.insert_membrane_report(hidden_report)
                console.print(f"  hidden: {hidden_report.passed}/{hidden_report.total}")

    # Report
    table = Table(title=f"{EXPERIMENT_ID} — slugify divergence at temperature=0")
    table.add_column("arm")
    table.add_column("n", justify="right")
    table.add_column("mean pairwise hamming", justify="right")
    table.add_column("hidden pass rate", justify="right")
    table.add_column("cost $", justify="right")

    for arm in ARMS:
        vectors = store.pass_vectors(EXPERIMENT_ID, arm.arm_id, SUBJECT, "hidden")
        n = len(vectors)
        div = mean_pairwise_hamming(vectors) if n >= 2 else 0.0
        pr = pass_rate(vectors)
        cost_row = store.con.execute(
            "SELECT COALESCE(SUM(cost_usd), 0) FROM runs WHERE experiment_id=? AND arm_id=? AND subject=?",
            [EXPERIMENT_ID, arm.arm_id, SUBJECT],
        ).fetchone()
        cost = float(cost_row[0]) if cost_row else 0.0
        table.add_row(arm.arm_id, str(n), f"{div:.3f}", f"{pr:.3f}", f"{cost:.4f}")

    console.print(table)

    # Verdict
    a_vectors = store.pass_vectors(EXPERIMENT_ID, "A_control", SUBJECT, "hidden")
    a_div = mean_pairwise_hamming(a_vectors) if len(a_vectors) >= 2 else None

    console.print()
    if a_div is None:
        console.print("[yellow]insufficient data for verdict[/]")
    elif a_div == 0.0:
        console.print(
            "[yellow]VERDICT: A_control divergence = 0.000 at temp=0. "
            "E1 slugify convergence was sampling noise. "
            "E2 must use a synthetic novel task, not slugify.[/]"
        )
    else:
        console.print(
            f"[green]VERDICT: A_control divergence = {a_div:.3f} at temp=0. "
            "Residual interpretation variance persists at temp=0. "
            "E1 slugify result not dominated by sampling noise.[/]"
        )

    store.close()


if __name__ == "__main__":
    run_diag()
