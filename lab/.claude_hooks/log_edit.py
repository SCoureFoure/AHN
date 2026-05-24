"""PostToolUse hook — log Edit/Write events to telemetry DB.

Opt-in via AHNLAB_TELEMETRY=1. Silent no-op otherwise.

Receives a JSON envelope on stdin describing the tool call. We only persist a
minimal signal: timestamp, session id, file path, tool name, lines changed.

Designed to be cheap and non-blocking. On any error, exits 0 with no output so
Claude Code is not affected.
"""
from __future__ import annotations

import json
import os
import sys
import time
from pathlib import Path


def main() -> int:
    if os.getenv("AHNLAB_TELEMETRY") != "1":
        return 0

    try:
        payload = json.loads(sys.stdin.read() or "{}")
    except Exception:
        return 0

    tool_input = payload.get("tool_input") or {}
    file_path = tool_input.get("file_path") or ""
    tool_name = payload.get("tool_name") or ""

    # Lazy import — only if telemetry enabled.
    try:
        import duckdb
    except Exception:
        return 0

    repo_root = Path(__file__).resolve().parents[2]
    db_path = repo_root / "lab" / "runs" / "claude_telemetry.duckdb"
    db_path.parent.mkdir(parents=True, exist_ok=True)

    try:
        con = duckdb.connect(str(db_path))
        con.execute("""
            CREATE TABLE IF NOT EXISTS edits (
                ts DOUBLE,
                session_id TEXT,
                tool_name TEXT,
                file_path TEXT,
                cwd TEXT
            )
        """)
        con.execute(
            "INSERT INTO edits VALUES (?, ?, ?, ?, ?)",
            [
                time.time(),
                os.getenv("CLAUDE_SESSION_ID", ""),
                tool_name,
                file_path,
                os.getcwd(),
            ],
        )
        con.close()
    except Exception:
        return 0

    return 0


if __name__ == "__main__":
    sys.exit(main())
