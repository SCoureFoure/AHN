# ahnlab

Experimentation lab for the Agentic Hierarchy of Needs framework. See `docs/00-intent.md`.

## Setup

```bash
cd lab
python -m venv .venv
. .venv/Scripts/activate    # PowerShell: .venv\Scripts\Activate.ps1
pip install -e .
cp .env.example .env        # then add ANTHROPIC_API_KEY
ahnlab init
```

## Run E1

```bash
ahnlab run --experiment E1
ahnlab report --experiment E1
```

## Layout

- `docs/` — intent, shared requirements, per-experiment requirements
- `src/ahnlab/` — harness, runner, store, arms, CLI
- `experiments/EN/subjects/` — task definitions and contracts for each subject in experiment N
- `experiments/EN/hidden/` — hidden judge suite for scoring outputs (agent never sees these)
- `tests/lab/` — contracts on the lab itself (AEs from `docs/01-shared-requirements.md`)
- `runs/` — DuckDB store + per-run artifact directories (gitignored)
