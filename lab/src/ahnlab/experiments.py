"""Built-in experiment specs."""
from __future__ import annotations

from pathlib import Path

from .config import LAB_ROOT
from .models import ArmSpec, ExperimentSpec


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


def e1_paths() -> tuple[Path, Path]:
    return (
        LAB_ROOT / "experiments" / "E1" / "subjects",
        LAB_ROOT / "experiments" / "E1" / "hidden",
    )


REGISTRY = {
    "E1": (e1_spec, e1_paths),
}
