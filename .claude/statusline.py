"""Status line — shows model, cache hit ratio, telemetry state.

Receives a JSON envelope on stdin from Claude Code. Returns a short string.
Failure-tolerant: any exception falls back to a minimal line.
"""
from __future__ import annotations

import json
import os
import sys


def main() -> int:
    try:
        payload = json.loads(sys.stdin.read() or "{}")
    except Exception:
        payload = {}

    model = (payload.get("model") or {}).get("display_name") or os.getenv("ANTHROPIC_MODEL", "unknown")
    usage = payload.get("current_usage") or {}
    cache_read = int(usage.get("cache_read_input_tokens", 0) or 0)
    cache_create = int(usage.get("cache_creation_input_tokens", 0) or 0)
    input_tok = int(usage.get("input_tokens", 0) or 0)

    total_in = cache_read + cache_create + input_tok
    cache_ratio = (cache_read / total_in * 100) if total_in > 0 else 0.0

    tele = "tele:on" if os.getenv("AHNLAB_TELEMETRY") == "1" else "tele:off"

    print(f"[{model}] cache:{cache_ratio:.0f}% | {tele}", end="")
    return 0


if __name__ == "__main__":
    sys.exit(main())
