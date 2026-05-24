# ahnlab — Lab Conventions

You are working inside the AHN experimentation lab. Read `lab/docs/00-intent.md` and `lab/BUILDLOG.md` before non-trivial changes.

## What the lab is for

Producing falsifiable measurements against the AHN framework (`documents/03-the-hypothesis.md`). Every component exists to support an experiment in `lab/docs/req-EN.md`.

## Layout

- `lab/src/ahnlab/` — harness, runner, store, arms, CLI
- `lab/experiments/EN/subjects/` — task definitions + contracts per subject
- `lab/experiments/EN/hidden/` — hidden judge suite (agent never sees these during runs)
- `lab/tests/lab/` — contracts on the lab components themselves
- `lab/runs/` — DuckDB store + per-run artifact dirs (gitignored)
- `lab/docs/` — intent + per-experiment requirements

## Discipline

- **Bootstrap exceptions are tracked, not hidden.** If you deviate from AHN red-green-refactor here, add a `lab/BUILDLOG.md` entry.
- **Acceptance examples in `lab/docs/req-EN.md` are the source of truth.** Tests derive from them. Implementation satisfies the tests.
- **No agent edits to `lab/experiments/EN/hidden/*` during an experiment run.** The hidden judge suite is the membrane for that experiment. It is below the implementation layer of the subjects.
- **Smoke tests stay green.** `pytest tests/lab -q` must pass after any change to `lab/src/ahnlab/`.

## Commands

- `pytest tests/lab -q` — smoke tests
- `ahnlab init` — create DuckDB + dirs
- `ahnlab run --experiment EN --trials N` — execute experiment
- `ahnlab report --experiment EN` — aggregate report

## Stack (do not introduce alternatives without recording the change)

- Python 3.11+
- `anthropic` SDK — Messages API + Batches
- `pytest` + `pytest-json-report` — programmatic membrane
- `pydantic` v2 — typed configs and rubrics
- `duckdb` — results store
- `rich` — CLI output
- `python-dotenv` — env loading
