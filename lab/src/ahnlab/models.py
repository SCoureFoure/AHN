"""Pydantic data models for the lab."""
from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, Field


TerminalStatus = Literal["ok", "api_error", "timeout", "max_tokens", "tool_error", "unknown"]


class TaskSpec(BaseModel):
    """Definition of a single agent task."""

    task_id: str
    subject: str
    intent_text: str
    model: str
    max_tokens: int = 4096
    temperature: float = 0.7
    system_prompt: str | None = None
    contract_files: list[Path] = Field(default_factory=list)
    extra_files: list[Path] = Field(default_factory=list)


class RunRecord(BaseModel):
    """Result of one agent task execution."""

    run_id: str
    task_id: str
    subject: str
    experiment_id: str
    arm_id: str
    seed: int
    model: str
    started_at: datetime
    ended_at: datetime
    input_tokens: int = 0
    output_tokens: int = 0
    cost_usd: float = 0.0
    cost_table_version: str = "2026-05"
    terminal_status: TerminalStatus = "unknown"
    error_reason: str | None = None
    transcript_path: Path
    artifacts_dir: Path
    api_request_id: str | None = None
    prompt_hash: str
    lab_git_sha: str | None = None
    lockfile_hash: str | None = None
    cycle_num: int = 0
    chain_id: str | None = None


class ContractResult(BaseModel):
    name: str
    status: Literal["passed", "failed", "error", "timeout", "skipped"]
    duration_s: float
    message: str | None = None


class MembraneReport(BaseModel):
    run_id: str
    suite_label: str  # "contracts" or "hidden"
    results: list[ContractResult]
    total: int
    passed: int
    failed: int
    errors: int
    timeouts: int
    duration_s: float

    @property
    def pass_vector(self) -> list[int]:
        """Ordered 1/0 vector of pass/fail per test, sorted by name."""
        return [1 if r.status == "passed" else 0 for r in sorted(self.results, key=lambda x: x.name)]


class CycleSpec(BaseModel):
    """Definition of one cycle in a multi-cycle experiment."""
    cycle_num: int
    intent_path: Path
    seed_path: Path
    contract_path: Path | None = None
    hidden_paths: list[Path] = Field(default_factory=list)


class MultiCycleArmSpec(BaseModel):
    arm_id: str
    description: str
    include_contracts: bool


class MultiCycleExperimentSpec(BaseModel):
    experiment_id: str
    description: str
    subject: str
    arms: list[MultiCycleArmSpec]
    cycles: list[CycleSpec]
    trials_per_arm: int
    model: str
    seed_schedule: list[int]


class MultiFileCycleSpec(BaseModel):
    """One cycle in a multi-file experiment — seed is a directory of .py files."""
    cycle_num: int
    intent_path: Path
    seed_dir: Path
    contract_path: Path | None = None
    hidden_paths: list[Path] = Field(default_factory=list)


class MultiFileExperimentSpec(BaseModel):
    experiment_id: str
    description: str
    subject: str
    arms: list[MultiCycleArmSpec]
    cycles: list[MultiFileCycleSpec]
    trials_per_arm: int
    model: str
    seed_schedule: list[int]


class ArmSpec(BaseModel):
    arm_id: str
    description: str
    include_contracts: bool
    contract_filenames: list[str] = Field(default_factory=list)
    """Explicit contract filenames (relative to subject dir). If empty and include_contracts=True, falls back to glob contracts*.py."""


class ExperimentSpec(BaseModel):
    experiment_id: str
    description: str
    subjects: list[str]
    arms: list[ArmSpec]
    trials_per_arm: int
    model: str
    seed_schedule: list[int]


def utcnow() -> datetime:
    return datetime.now(timezone.utc)
