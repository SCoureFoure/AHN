"""Smoke tests for the store — uses an in-memory-style temp file."""
from datetime import datetime, timezone
from pathlib import Path

import pytest

from ahnlab.models import ContractResult, MembraneReport, RunRecord
from ahnlab.store import Store


@pytest.fixture()
def store(tmp_path: Path):
    s = Store(tmp_path / "t.duckdb")
    yield s
    s.close()


def _run(run_id: str, experiment_id: str = "E1", arm_id: str = "A_control", subject: str = "is_prime") -> RunRecord:
    now = datetime.now(timezone.utc)
    return RunRecord(
        run_id=run_id, task_id="t", subject=subject, experiment_id=experiment_id, arm_id=arm_id,
        seed=1, model="claude-haiku-4-5-20251001", started_at=now, ended_at=now,
        transcript_path=Path("x"), artifacts_dir=Path("y"), prompt_hash="abc",
    )


def test_schema_idempotent(tmp_path: Path):
    s1 = Store(tmp_path / "t.duckdb")
    s1.close()
    s2 = Store(tmp_path / "t.duckdb")
    s2.close()


def test_insert_and_count(store: Store):
    store.upsert_experiment("E1", "test", "{}")
    store.upsert_arm("E1", "A_control", "", False)
    store.insert_run(_run("r1"))
    store.insert_run(_run("r2"))
    assert store.count_runs("E1", "A_control", "is_prime") == 2


def test_membrane_report_pass_vector_roundtrip(store: Store):
    store.upsert_experiment("E1", "test", "{}")
    store.upsert_arm("E1", "A_control", "", False)
    store.insert_run(_run("r1"))
    report = MembraneReport(
        run_id="r1", suite_label="hidden",
        results=[
            ContractResult(name="t_a", status="passed", duration_s=0.01),
            ContractResult(name="t_b", status="failed", duration_s=0.01),
            ContractResult(name="t_c", status="passed", duration_s=0.01),
        ],
        total=3, passed=2, failed=1, errors=0, timeouts=0, duration_s=0.03,
    )
    store.insert_membrane_report(report)
    vectors = store.pass_vectors("E1", "A_control", "is_prime", "hidden")
    assert vectors == [[1, 0, 1]]
