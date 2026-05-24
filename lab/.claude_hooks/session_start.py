"""SessionStart hook — record session config snapshot.

Opt-in via AHNLAB_TELEMETRY=1. Silent no-op otherwise.

Captures: session id, model, git SHA, hash of root CLAUDE.md and rules manifest.
Lets us later correlate outcomes (edit count, cost, error rate) with config.
"""
from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
import time
from pathlib import Path


def _file_hash(p: Path) -> str:
    if not p.exists():
        return ""
    return hashlib.sha256(p.read_bytes()).hexdigest()[:16]


def _git_sha(cwd: Path) -> str:
    try:
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=cwd, capture_output=True, text=True, timeout=2,
        )
        if result.returncode == 0:
            return result.stdout.strip()
    except Exception:
        pass
    return ""


def main() -> int:
    if os.getenv("AHNLAB_TELEMETRY") != "1":
        return 0

    try:
        import duckdb
    except Exception:
        return 0

    repo_root = Path(__file__).resolve().parents[2]
    db_path = repo_root / "lab" / "runs" / "claude_telemetry.duckdb"
    db_path.parent.mkdir(parents=True, exist_ok=True)

    claude_md = repo_root / ".claude" / "CLAUDE.md"
    rules_manifest = json.dumps(sorted(
        str(p.relative_to(repo_root)) for p in (repo_root / ".claude" / "rules").glob("*.md")
    )) if (repo_root / ".claude" / "rules").exists() else "[]"

    try:
        con = duckdb.connect(str(db_path))
        con.execute("""
            CREATE TABLE IF NOT EXISTS sessions (
                ts DOUBLE,
                session_id TEXT,
                git_sha TEXT,
                claude_md_hash TEXT,
                rules_manifest TEXT,
                env_telemetry TEXT
            )
        """)
        con.execute(
            "INSERT INTO sessions VALUES (?, ?, ?, ?, ?, ?)",
            [
                time.time(),
                os.getenv("CLAUDE_SESSION_ID", ""),
                _git_sha(repo_root),
                _file_hash(claude_md),
                rules_manifest,
                os.getenv("AHNLAB_TELEMETRY", ""),
            ],
        )
        con.close()
    except Exception:
        return 0

    return 0


if __name__ == "__main__":
    sys.exit(main())
