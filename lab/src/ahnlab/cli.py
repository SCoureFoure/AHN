"""R7 CLI — entrypoint `ahnlab`."""
from __future__ import annotations

import argparse
import sys

from rich.console import Console
from rich.table import Table

from .arms import execute
from .config import DB_PATH, ANTHROPIC_API_KEY, ensure_dirs
from .cycle_runner import execute_cycles, execute_multi_file_cycles
from .experiments import REGISTRY
from .metrics import mean_pairwise_hamming, pass_rate
from .models import MultiCycleExperimentSpec, MultiFileExperimentSpec
from .store import Store


console = Console()


def cmd_init(_args: argparse.Namespace) -> int:
    ensure_dirs()
    store = Store()
    console.print(f"[green]initialized[/] db at {DB_PATH}")
    store.close()
    return 0


def cmd_run(args: argparse.Namespace) -> int:
    if not ANTHROPIC_API_KEY:
        console.print("[red]ANTHROPIC_API_KEY missing[/] — set it in .env at lab root")
        return 2
    if args.experiment not in REGISTRY:
        console.print(f"[red]unknown experiment[/] {args.experiment}")
        return 2
    spec_fn, paths_fn = REGISTRY[args.experiment]
    spec = spec_fn(trials_per_arm=args.trials, model=args.model) if args.model else spec_fn(trials_per_arm=args.trials)
    subjects_root = paths_fn()

    ensure_dirs()
    store = Store()
    try:
        if isinstance(spec, MultiFileExperimentSpec):
            execute_multi_file_cycles(spec, subjects_root, store)
        elif isinstance(spec, MultiCycleExperimentSpec):
            execute_cycles(spec, subjects_root, store)
        else:
            execute(spec, subjects_root, store)
    finally:
        store.close()

    store = Store()
    try:
        if isinstance(spec, (MultiCycleExperimentSpec, MultiFileExperimentSpec)):
            for arm in spec.arms:
                count = store.count_chains(spec.experiment_id, arm.arm_id, spec.subject)
                if count < spec.trials_per_arm:
                    console.print(f"[yellow]arm under-trialled[/] {arm.arm_id}: {count}/{spec.trials_per_arm} chains")
                    return 1
        else:
            for arm in spec.arms:
                for subject in spec.subjects:
                    count = store.count_runs(spec.experiment_id, arm.arm_id, subject)
                    if count < spec.trials_per_arm:
                        console.print(f"[yellow]arm under-trialled[/] {arm.arm_id} subj={subject}: {count}/{spec.trials_per_arm}")
                        return 1
    finally:
        store.close()
    return 0


def cmd_report(args: argparse.Namespace) -> int:
    if args.experiment not in REGISTRY:
        console.print(f"[red]unknown experiment[/] {args.experiment}")
        return 2
    spec_fn, _ = REGISTRY[args.experiment]
    spec = spec_fn()

    store = Store()
    try:
        if isinstance(spec, (MultiCycleExperimentSpec, MultiFileExperimentSpec)):
            table = Table(title=f"{args.experiment} — hidden pass rate per (arm, cycle)")
            table.add_column("arm")
            table.add_column("cycle", justify="right")
            table.add_column("n", justify="right")
            table.add_column("hidden pass rate", justify="right")
            table.add_column("cost $", justify="right")
            for arm in spec.arms:
                for cycle in spec.cycles:
                    vectors = store.pass_vectors_by_cycle(spec.experiment_id, arm.arm_id, spec.subject, cycle.cycle_num)
                    n = len(vectors)
                    pr = pass_rate(vectors)
                    cost_row = store.con.execute(
                        "SELECT COALESCE(SUM(cost_usd), 0) FROM runs WHERE experiment_id=? AND arm_id=? AND cycle_num=?",
                        [spec.experiment_id, arm.arm_id, cycle.cycle_num],
                    ).fetchone()
                    cost = float(cost_row[0]) if cost_row else 0.0
                    table.add_row(arm.arm_id, f"c{cycle.cycle_num}", str(n), f"{pr:.3f}", f"{cost:.4f}")
        else:
            table = Table(title=f"{args.experiment} — divergence + pass rate per (arm, subject)")
            table.add_column("subject")
            table.add_column("arm")
            table.add_column("n", justify="right")
            table.add_column("mean pairwise hamming", justify="right")
            table.add_column("hidden pass rate", justify="right")
            table.add_column("cost $", justify="right")
            for subject in spec.subjects:
                for arm in spec.arms:
                    vectors = store.pass_vectors(spec.experiment_id, arm.arm_id, subject, "hidden")
                    n = len(vectors)
                    div = mean_pairwise_hamming(vectors) if n >= 2 else 0.0
                    pr = pass_rate(vectors)
                    cost_row = store.con.execute(
                        "SELECT COALESCE(SUM(cost_usd), 0) FROM runs WHERE experiment_id=? AND arm_id=? AND subject=?",
                        [spec.experiment_id, arm.arm_id, subject],
                    ).fetchone()
                    cost = float(cost_row[0]) if cost_row else 0.0
                    table.add_row(subject, arm.arm_id, str(n), f"{div:.3f}", f"{pr:.3f}", f"{cost:.4f}")
    finally:
        store.close()

    console.print(table)
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="ahnlab")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_init = sub.add_parser("init", help="initialize db + dirs")
    p_init.set_defaults(func=cmd_init)

    p_run = sub.add_parser("run", help="run an experiment")
    p_run.add_argument("--experiment", required=True)
    p_run.add_argument("--trials", type=int, default=30)
    p_run.add_argument("--model", default=None)
    p_run.set_defaults(func=cmd_run)

    p_report = sub.add_parser("report", help="report aggregate metrics")
    p_report.add_argument("--experiment", required=True)
    p_report.set_defaults(func=cmd_report)

    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
