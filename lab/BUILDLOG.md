# BUILDLOG — bootstrap exceptions

The framework says intent originates from a human and contracts precede implementation. This lab was built in co-authorship between a human and an agent under explicit time pressure for v1. The following deviations are recorded here so the lab's own results can later be examined against the conditions under which it was produced.

## Deviation 1 — Co-drafted intent and requirements

- `docs/00-intent.md`, `docs/01-shared-requirements.md`, and `docs/req-E1.md` were drafted in conversation. The agent proposed structure and acceptance examples; the human accepted them without independent restatement.
- The framework's "Law II — you cannot enforce downward without grounding upward" technically requires that intent precede requirements precede contracts. We collapsed these into a single co-authoring pass.

## Deviation 2 — Lab component contracts not fully encoded before impl

- Shared requirements R1..R7 carry acceptance examples in `docs/01-shared-requirements.md`.
- Only a subset (R2 membrane runner, R4 store via `tests/lab/test_*.py`, R-metrics) is encoded as executable contracts in v1.
- R1 (harness), R5 (arm controller), R6 (reproducibility), R7 (CLI) have no executable contracts yet. They were implemented from the requirement text directly.

## Deviation 3 — Single-pass implementation

- Components were written sequentially in one session rather than red-green-refactor against contracts.

## What this means for E1 results

If E1 produces the predicted result (Arm A divergence > Arm B divergence on ambiguous subjects), the deviation is harmless — the lab still produced a falsifiable measurement. If E1 produces the null or inverse result, the deviation joins the candidate explanation set alongside genuine theoretical refutation. It does not, by itself, refute the framework.

## Cleanup path

After E1 produces first data, prioritized cleanup:

1. Backfill executable contracts for R1, R5, R6, R7 from existing AEs.
2. Replace single-pass impl with red-green-refactor for any future component.
3. Document the human's independent restatement of intent before E2..E8.
