"""R4 Results Store — DuckDB persistence for runs and reports."""
from __future__ import annotations

import json
from pathlib import Path

import duckdb

from .config import DB_PATH
from .models import ContractResult, MembraneReport, RunRecord


SCHEMA = """
CREATE TABLE IF NOT EXISTS experiments (
    experiment_id TEXT PRIMARY KEY,
    description TEXT,
    config_json TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS arms (
    experiment_id TEXT,
    arm_id TEXT,
    description TEXT,
    include_contracts BOOLEAN,
    PRIMARY KEY (experiment_id, arm_id)
);

CREATE TABLE IF NOT EXISTS runs (
    run_id TEXT PRIMARY KEY,
    task_id TEXT,
    subject TEXT,
    experiment_id TEXT,
    arm_id TEXT,
    seed INTEGER,
    model TEXT,
    started_at TIMESTAMP,
    ended_at TIMESTAMP,
    input_tokens INTEGER,
    output_tokens INTEGER,
    cost_usd DOUBLE,
    cost_table_version TEXT,
    terminal_status TEXT,
    error_reason TEXT,
    transcript_path TEXT,
    artifacts_dir TEXT,
    api_request_id TEXT,
    prompt_hash TEXT,
    lab_git_sha TEXT,
    lockfile_hash TEXT,
    cycle_num INTEGER DEFAULT 0,
    chain_id TEXT
);

CREATE TABLE IF NOT EXISTS membrane_reports (
    run_id TEXT,
    suite_label TEXT,
    total INTEGER,
    passed INTEGER,
    failed INTEGER,
    errors INTEGER,
    timeouts INTEGER,
    duration_s DOUBLE,
    pass_vector TEXT,
    results_json TEXT,
    PRIMARY KEY (run_id, suite_label)
);
"""


class Store:
    def __init__(self, path: Path | None = None) -> None:
        self.path = Path(path or DB_PATH)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.con = duckdb.connect(str(self.path))
        self._init_schema()

    def _init_schema(self) -> None:
        for stmt in SCHEMA.strip().split(";"):
            s = stmt.strip()
            if s:
                self.con.execute(s)
        # Migrate existing runs table to add cycle columns if absent.
        cols = {r[0] for r in self.con.execute("DESCRIBE runs").fetchall()}
        if "cycle_num" not in cols:
            self.con.execute("ALTER TABLE runs ADD COLUMN cycle_num INTEGER DEFAULT 0")
        if "chain_id" not in cols:
            self.con.execute("ALTER TABLE runs ADD COLUMN chain_id TEXT")

    def close(self) -> None:
        self.con.close()

    def upsert_experiment(self, experiment_id: str, description: str, config_json: str) -> None:
        self.con.execute(
            "INSERT OR REPLACE INTO experiments (experiment_id, description, config_json) VALUES (?, ?, ?)",
            [experiment_id, description, config_json],
        )

    def upsert_arm(self, experiment_id: str, arm_id: str, description: str, include_contracts: bool) -> None:
        self.con.execute(
            "INSERT OR REPLACE INTO arms (experiment_id, arm_id, description, include_contracts) VALUES (?, ?, ?, ?)",
            [experiment_id, arm_id, description, include_contracts],
        )

    def insert_run(self, r: RunRecord) -> None:
        self.con.execute(
            """
            INSERT INTO runs (
                run_id, task_id, subject, experiment_id, arm_id, seed, model,
                started_at, ended_at, input_tokens, output_tokens, cost_usd,
                cost_table_version, terminal_status, error_reason,
                transcript_path, artifacts_dir, api_request_id, prompt_hash,
                lab_git_sha, lockfile_hash, cycle_num, chain_id
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            [
                r.run_id, r.task_id, r.subject, r.experiment_id, r.arm_id, r.seed, r.model,
                r.started_at, r.ended_at, r.input_tokens, r.output_tokens, r.cost_usd,
                r.cost_table_version, r.terminal_status, r.error_reason,
                str(r.transcript_path), str(r.artifacts_dir), r.api_request_id, r.prompt_hash,
                r.lab_git_sha, r.lockfile_hash, r.cycle_num, r.chain_id,
            ],
        )

    def insert_membrane_report(self, report: MembraneReport) -> None:
        self.con.execute(
            """
            INSERT OR REPLACE INTO membrane_reports (
                run_id, suite_label, total, passed, failed, errors, timeouts,
                duration_s, pass_vector, results_json
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            [
                report.run_id, report.suite_label, report.total, report.passed,
                report.failed, report.errors, report.timeouts, report.duration_s,
                json.dumps(report.pass_vector),
                json.dumps([r.model_dump() for r in report.results]),
            ],
        )

    def count_runs(self, experiment_id: str, arm_id: str | None = None, subject: str | None = None) -> int:
        clauses = ["experiment_id = ?"]
        params: list = [experiment_id]
        if arm_id is not None:
            clauses.append("arm_id = ?")
            params.append(arm_id)
        if subject is not None:
            clauses.append("subject = ?")
            params.append(subject)
        sql = f"SELECT COUNT(*) FROM runs WHERE {' AND '.join(clauses)}"
        return int(self.con.execute(sql, params).fetchone()[0])

    def runs_for(self, experiment_id: str, arm_id: str, subject: str) -> list[dict]:
        rows = self.con.execute(
            "SELECT run_id, terminal_status FROM runs WHERE experiment_id = ? AND arm_id = ? AND subject = ?",
            [experiment_id, arm_id, subject],
        ).fetchall()
        return [{"run_id": r[0], "terminal_status": r[1]} for r in rows]

    def pass_vectors_by_cycle(self, experiment_id: str, arm_id: str, subject: str, cycle_num: int, suite_label: str = "hidden") -> list[list[int]]:
        rows = self.con.execute(
            """
            SELECT mr.pass_vector
            FROM membrane_reports mr
            JOIN runs r ON r.run_id = mr.run_id
            WHERE r.experiment_id = ? AND r.arm_id = ? AND r.subject = ?
              AND r.cycle_num = ? AND mr.suite_label = ?
            """,
            [experiment_id, arm_id, subject, cycle_num, suite_label],
        ).fetchall()
        return [json.loads(r[0]) for r in rows]

    def count_chains(self, experiment_id: str, arm_id: str, subject: str) -> int:
        row = self.con.execute(
            "SELECT COUNT(DISTINCT chain_id) FROM runs WHERE experiment_id=? AND arm_id=? AND subject=? AND chain_id IS NOT NULL",
            [experiment_id, arm_id, subject],
        ).fetchone()
        return int(row[0]) if row else 0

    def pass_vectors(self, experiment_id: str, arm_id: str, subject: str, suite_label: str = "hidden") -> list[list[int]]:
        rows = self.con.execute(
            """
            SELECT mr.pass_vector
            FROM membrane_reports mr
            JOIN runs r ON r.run_id = mr.run_id
            WHERE r.experiment_id = ? AND r.arm_id = ? AND r.subject = ?
              AND mr.suite_label = ?
            """,
            [experiment_id, arm_id, subject, suite_label],
        ).fetchall()
        return [json.loads(r[0]) for r in rows]
