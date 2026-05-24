"""Lab configuration. Loaded from env."""
from __future__ import annotations

import os
import subprocess
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

LAB_ROOT = Path(__file__).resolve().parents[2]
DB_PATH = Path(os.getenv("AHNLAB_DB_PATH", LAB_ROOT / "runs" / "ahnlab.duckdb"))
RUNS_DIR = Path(os.getenv("AHNLAB_RUNS_DIR", LAB_ROOT / "runs"))
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

# Pricing: $/MTok as of 2026-05. Keep table tiny; extend as needed.
PRICE_TABLE_VERSION = "2026-05"
PRICE_TABLE_USD_PER_MTOK = {
    "claude-haiku-4-5-20251001": {"input": 1.00, "output": 5.00},
    "claude-sonnet-4-6": {"input": 3.00, "output": 15.00},
    "claude-opus-4-7": {"input": 15.00, "output": 75.00},
}


def lab_git_sha() -> str | None:
    try:
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=LAB_ROOT,
            capture_output=True,
            text=True,
            timeout=2,
        )
        if result.returncode == 0:
            return result.stdout.strip()
    except Exception:
        pass
    return None


def ensure_dirs() -> None:
    RUNS_DIR.mkdir(parents=True, exist_ok=True)
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)


def compute_cost_usd(model: str, input_tokens: int, output_tokens: int) -> float:
    prices = PRICE_TABLE_USD_PER_MTOK.get(model)
    if prices is None:
        return 0.0
    return (input_tokens * prices["input"] + output_tokens * prices["output"]) / 1_000_000
