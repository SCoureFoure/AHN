---
description: Run an AHN lab experiment with cost guard. Usage: /lab-run <experiment-id> [trials]
argument-hint: <experiment-id> [trials=30]
---

# /lab-run

Run an AHN lab experiment.

Before running:

1. Read `lab/BUILDLOG.md` to understand current bootstrap exception state.
2. Confirm `ANTHROPIC_API_KEY` is set in `lab/.env`.
3. If `$2` (trials) is greater than 50, stop and ask the user to confirm — Haiku at N=180 trials is roughly $0.10, but Sonnet at the same scale crosses $1, and the user should make the cost call explicitly.

Then execute:

```bash
cd lab && ahnlab run --experiment $1 --trials ${2:-30}
```

After it finishes:

```bash
cd lab && ahnlab report --experiment $1
```

Report the per-arm divergence and pass rate inline. Do not invent metric interpretations — the report's columns are: `subject`, `arm`, `n`, `mean pairwise hamming`, `hidden pass rate`, `cost $`. Read them literally.

If the run errors, surface the first traceback line and stop. Do not retry.
