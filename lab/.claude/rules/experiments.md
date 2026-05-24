---
paths:
  - "lab/experiments/**"
  - "lab/docs/req-*.md"
---

# Experiment Authoring Rules

When working under `lab/experiments/` or in a `lab/docs/req-EN.md` file:

## Subjects

- One subject = one self-contained problem with a single intent.md, one contracts.py (Arm B's contracts), and one hidden suite under `lab/experiments/EN/hidden/`.
- Hidden suite must be a **superset** of contracts. Every contract test must have a corresponding hidden test (renamed `test_hidden_*`). Hidden adds edge cases that surface interpretation drift.
- Hidden suite is **agent-invisible** at run time. The harness must never expose `lab/experiments/*/hidden/` to a session that will produce an artifact for scoring.

## Acceptance examples

- Every acceptance example is one of: a function call with expected return value, an input gesture with an expected output state, or a numeric threshold gated against a measurable quantity.
- Do not write acceptance examples that say things like "good error handling" — those are not examples, they are aspirations. Convert to: "calling with input X raises Y" or remove.

## Falsifiers

- Every `req-EN.md` must include a "Falsifiers for this experiment specifically" section. If the experiment's predicted result is not observed, this section is what the analyst checks before declaring the framework refuted.
- Falsifiers must be specific: thresholds, comparisons, ordering claims. "Result doesn't look right" is not a falsifier.

## Predicted results

- State the prediction in concrete terms before running. "Arm A divergence > Arm B divergence on Subject 2" is acceptable. "Things will be better with contracts" is not.
- Predictions go in `req-EN.md`, not in code comments. The analyst reads `req-EN.md` to compare observation against prediction.

## Costs and trials

- Default trials per arm = 30. Increase only after pilot shows variance demands it. Decrease to 3-5 for dry runs / smoke validation.
- Pilot every new experiment at trials=3 before running at full N.
- Record cost per trial in the report. Cost-per-correct-feature is a primary metric for E7.
