---
paths:
  - "lab/**/*.py"
---

# Lab Python Conventions

- **Python 3.11+.** Use `from __future__ import annotations` at file head where forward refs help.
- **Type hints required** on public functions (anything not prefixed with `_`).
- **Pydantic v2 models** for any structured data crossing a boundary (CLI input, hook input, DB row).
- **`pathlib.Path` over `os.path`** everywhere.
- **No bare `except:`.** Catch specific exception types. Hook scripts may broadly except + return 0 (their failure must not break Claude Code) — document that pattern with a comment.
- **Subprocess timeouts mandatory.** Every `subprocess.run` must specify `timeout=`.
- **No print() in library code.** Use `rich.console` or return values. Hook scripts and CLI commands may print.
- **Tests live in `lab/tests/lab/`**, named `test_*.py`. Use pytest fixtures for tmp dirs.
- **DuckDB connections are explicit.** Open in a context-managed pattern or call `.close()`. Read-only access uses `read_only=True`.
- **Anthropic SDK errors:** catch `APIError` / `APIStatusError` and convert to a `RunRecord` with `terminal_status="api_error"`. Never let an API failure raise out of the harness — that breaks the arm controller's isolation guarantee.
- **Cost capture is non-negotiable.** Every API call must record `input_tokens`, `output_tokens`, and computed cost against the versioned price table in `config.py`.
