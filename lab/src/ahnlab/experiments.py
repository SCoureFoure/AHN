"""Built-in experiment specs."""
from __future__ import annotations

from pathlib import Path

from .config import SUBJECTS_ROOT
from .models import ArmSpec, CycleSpec, ExperimentSpec, MultiCycleArmSpec, MultiCycleExperimentSpec, MultiFileCycleSpec, MultiFileExperimentSpec


DEFAULT_MODEL = "claude-haiku-4-5-20251001"


def e1_spec(trials_per_arm: int = 30, model: str = DEFAULT_MODEL) -> ExperimentSpec:
    return ExperimentSpec(
        experiment_id="E1",
        description="Interpretation variance — same intent, with vs without contracts.",
        subjects=["is_prime", "slugify", "summarize"],
        arms=[
            ArmSpec(arm_id="A_control", description="Intent only, no contracts.", include_contracts=False),
            ArmSpec(arm_id="B_contracts", description="Intent + failing acceptance tests.", include_contracts=True),
        ],
        trials_per_arm=trials_per_arm,
        model=model,
        seed_schedule=list(range(1, trials_per_arm + 1)),
    )


def e1_paths() -> Path:
    return SUBJECTS_ROOT


def e2_spec(trials_per_arm: int = 100, model: str = DEFAULT_MODEL) -> ExperimentSpec:
    return ExperimentSpec(
        experiment_id="E2",
        description="Contract completeness — 4-arm (0%, partial, partial+warning, full) on normalize_tags.",
        subjects=["normalize_tags"],
        arms=[
            ArmSpec(
                arm_id="A_zero",
                description="Intent only, no contracts.",
                include_contracts=False,
            ),
            ArmSpec(
                arm_id="B_partial",
                description="Intent + 2 basic acceptance examples (happy path only).",
                include_contracts=True,
                contract_filenames=["contracts_B.py"],
            ),
            ArmSpec(
                arm_id="C_partial_warn",
                description="Intent + 2 basic AEs + explicit incompleteness warning.",
                include_contracts=True,
                contract_filenames=["contracts_C.py"],
            ),
            ArmSpec(
                arm_id="D_full",
                description="Intent + all 9 acceptance examples (full edge-case coverage).",
                include_contracts=True,
                contract_filenames=["contracts_D.py"],
            ),
        ],
        trials_per_arm=trials_per_arm,
        model=model,
        seed_schedule=list(range(1, trials_per_arm + 1)),
    )


def e2_paths() -> Path:
    return SUBJECTS_ROOT


def e2b_spec(trials_per_arm: int = 30, model: str = DEFAULT_MODEL) -> ExperimentSpec:
    # E2 family: contract completeness extension probing C_partial_warn mechanism
    # and B_partial inversion on a wrong-default subject. Subject validation failed
    # (A_zero=1.000) — group_by_prefix not a wrong-default task for Haiku 4.5.
    return ExperimentSpec(
        experiment_id="E2b",
        description="E2 extension — contract completeness on group_by_prefix (subject failed A_zero validation: too capable).",
        subjects=["group_by_prefix"],
        arms=[
            ArmSpec(
                arm_id="A_zero",
                description="Intent only, no contracts.",
                include_contracts=False,
            ),
            ArmSpec(
                arm_id="B_partial",
                description="Intent + 2 basic AEs (happy path only).",
                include_contracts=True,
                contract_filenames=["contracts_B.py"],
            ),
            ArmSpec(
                arm_id="C_partial_warn",
                description="Intent + 2 basic AEs + explicit incompleteness warning.",
                include_contracts=True,
                contract_filenames=["contracts_C.py"],
            ),
            ArmSpec(
                arm_id="D_full",
                description="Intent + all 9 acceptance examples (full edge-case coverage).",
                include_contracts=True,
                contract_filenames=["contracts_D.py"],
            ),
        ],
        trials_per_arm=trials_per_arm,
        model=model,
        seed_schedule=list(range(1, trials_per_arm + 1)),
    )


def e2b_paths() -> Path:
    return SUBJECTS_ROOT


def e2c_spec(trials_per_arm: int = 30, model: str = DEFAULT_MODEL) -> ExperimentSpec:
    # E2 family: alternate wrong-default subject. Subject validation also failed
    # (A_zero=1.000) — invert_index not a wrong-default task for Haiku 4.5 either.
    return ExperimentSpec(
        experiment_id="E2c",
        description="E2 extension — contract completeness on invert_index (subject failed A_zero validation: too capable).",
        subjects=["invert_index"],
        arms=[
            ArmSpec(
                arm_id="A_zero",
                description="Intent only, no contracts.",
                include_contracts=False,
            ),
            ArmSpec(
                arm_id="B_partial",
                description="Intent + 2 basic AEs (happy path only).",
                include_contracts=True,
                contract_filenames=["contracts_B.py"],
            ),
            ArmSpec(
                arm_id="C_partial_warn",
                description="Intent + 2 basic AEs + explicit incompleteness warning.",
                include_contracts=True,
                contract_filenames=["contracts_C.py"],
            ),
            ArmSpec(
                arm_id="D_full",
                description="Intent + all 9 acceptance examples (full edge-case coverage).",
                include_contracts=True,
                contract_filenames=["contracts_D.py"],
            ),
        ],
        trials_per_arm=trials_per_arm,
        model=model,
        seed_schedule=list(range(1, trials_per_arm + 1)),
    )


def e2c_paths() -> Path:
    return SUBJECTS_ROOT


def e3_spec(trials_per_arm: int = 10, model: str = DEFAULT_MODEL) -> MultiCycleExperimentSpec:
    todo = SUBJECTS_ROOT / "todo_list"
    cycles = [
        CycleSpec(
            cycle_num=n,
            intent_path=todo / "cycles" / f"c{n}" / "intent.md",
            seed_path=todo / "seeds" / f"c{n}_seed.py",
            contract_path=todo / "cycles" / f"c{n}" / "contracts.py",
            hidden_paths=sorted((todo / "hidden").glob(f"hidden_c{n}.py")),
        )
        for n in range(1, 5)
    ]
    return MultiCycleExperimentSpec(
        experiment_id="E3",
        description="Compounding regression — hierarchy-first vs free-edit across 4 feature cycles on todo_list.",
        subject="todo_list",
        arms=[
            MultiCycleArmSpec(arm_id="A_free", description="No contracts at any cycle.", include_contracts=False),
            MultiCycleArmSpec(arm_id="B_hierarchy", description="Cumulative contracts at each cycle.", include_contracts=True),
        ],
        cycles=cycles,
        trials_per_arm=trials_per_arm,
        model=model,
        seed_schedule=list(range(1, trials_per_arm + 1)),
    )


def e3_paths() -> Path:
    return SUBJECTS_ROOT


def e3b_spec(trials_per_arm: int = 10, model: str = DEFAULT_MODEL) -> MultiFileExperimentSpec:
    todo = SUBJECTS_ROOT / "todo_app"
    cycles = [
        MultiFileCycleSpec(
            cycle_num=n,
            intent_path=todo / "cycles" / f"c{n}" / "intent.md",
            seed_dir=todo / "seeds" / f"c{n}",
            contract_path=todo / "cycles" / f"c{n}" / "contracts.py",
            hidden_paths=sorted((todo / "hidden").glob(f"hidden_c{n}.py")),
        )
        for n in range(1, 5)
    ]
    return MultiFileExperimentSpec(
        experiment_id="E3b",
        description="Multi-file compounding regression — hierarchy-first vs free-edit across 4 feature cycles on todo_app.",
        subject="todo_app",
        arms=[
            MultiCycleArmSpec(arm_id="A_free", description="No contracts at any cycle.", include_contracts=False),
            MultiCycleArmSpec(arm_id="B_hierarchy", description="Cumulative contracts at each cycle.", include_contracts=True),
        ],
        cycles=cycles,
        trials_per_arm=trials_per_arm,
        model=model,
        seed_schedule=list(range(1, trials_per_arm + 1)),
    )


def e3b_paths() -> Path:
    return SUBJECTS_ROOT


REGISTRY = {
    "E1": (e1_spec, e1_paths),
    "E2": (e2_spec, e2_paths),
    "E2b": (e2b_spec, e2b_paths),
    "E2c": (e2c_spec, e2c_paths),
    "E3": (e3_spec, e3_paths),
    "E3b": (e3b_spec, e3b_paths),
}
