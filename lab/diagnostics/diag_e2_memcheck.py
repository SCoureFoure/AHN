"""Memorization check for E2 subject normalize_tags.

Runs 5 trials of A_zero at temperature=0. If hamming=0.000, subject is
memorized and E2 design is invalid — pick a different subject.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from anthropic import Anthropic
from rich.console import Console

from ahnlab.config import ANTHROPIC_API_KEY, RUNS_DIR, ensure_dirs
from ahnlab.harness import run_task
from ahnlab.membrane import run_suite
from ahnlab.metrics import mean_pairwise_hamming
from ahnlab.models import TaskSpec
from ahnlab.store import Store

EXPERIMENT_ID = "E2-MEMCHECK-T0"
SUBJECT = "normalize_tags"
N = 5
MODEL = "claude-haiku-4-5-20251001"
SEEDS = list(range(201, 201 + N))

SUBJECTS_ROOT = Path(__file__).resolve().parents[1] / "experiments" / "E2" / "subjects"
HIDDEN_ROOT = Path(__file__).resolve().parents[1] / "experiments" / "E2" / "hidden"

console = Console()


def run_memcheck() -> None:
    if not ANTHROPIC_API_KEY:
        console.print("[red]ANTHROPIC_API_KEY missing[/]")
        sys.exit(2)

    ensure_dirs()
    store = Store()
    store.upsert_experiment(EXPERIMENT_ID, "E2 memorization check: A_zero at temp=0", "{}")
    store.upsert_arm(EXPERIMENT_ID, "A_zero", "Intent only, no contracts.", False)

    subject_dir = SUBJECTS_ROOT / SUBJECT
    intent_text = (subject_dir / "intent.md").read_text(encoding="utf-8")
    hidden_files = sorted(HIDDEN_ROOT.glob(f"{SUBJECT}_hidden*.py"))

    client = Anthropic(api_key=ANTHROPIC_API_KEY)
    existing_count = store.count_runs(EXPERIMENT_ID, "A_zero", SUBJECT)
    skip = existing_count

    for seed in SEEDS:
        if skip > 0:
            skip -= 1
            continue
        console.print(f"[cyan]memcheck[/] seed={seed} temp=0")
        task = TaskSpec(
            task_id=f"{EXPERIMENT_ID}:{SUBJECT}:A_zero:{seed}",
            subject=SUBJECT,
            intent_text=intent_text,
            model=MODEL,
            temperature=0.0,
            contract_files=[],
        )
        try:
            rec = run_task(task, EXPERIMENT_ID, "A_zero", seed,
                           include_contracts=False, client=client)
        except Exception as e:
            console.print(f"[red]error[/] {e}")
            continue
        store.insert_run(rec)
        if hidden_files and rec.terminal_status == "ok":
            report = run_suite(rec.run_id, rec.artifacts_dir, hidden_files, "hidden")
            store.insert_membrane_report(report)
            console.print(f"  hidden: {report.passed}/{report.total} | vector: {report.pass_vector}")

    vectors = store.pass_vectors(EXPERIMENT_ID, "A_zero", SUBJECT, "hidden")
    n = len(vectors)
    div = mean_pairwise_hamming(vectors) if n >= 2 else None

    console.print()
    if div is None:
        console.print("[yellow]insufficient runs for verdict[/]")
    elif div == 0.0:
        console.print(
            "[red]FAIL: hamming=0.000 at temp=0. Subject is memorized. "
            "Pick a different subject for E2.[/]"
        )
        sys.exit(1)
    else:
        console.print(
            f"[green]PASS: hamming={div:.3f} at temp=0. Subject not memorized. "
            "E2 design is valid — proceed.[/]"
        )

    store.close()


if __name__ == "__main__":
    run_memcheck()
