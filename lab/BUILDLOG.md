# BUILDLOG — bootstrap exceptions

The framework says intent originates from a human and contracts precede implementation. This lab was built in co-authorship between a human and an agent(or agents) under explicit time pressure for v1. The following deviations are recorded here so the lab's own results can later be examined against the conditions under which it was produced.

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

## Deviation 4 — membrane.py pytest discovery bug (found during E1 pilot)

- `membrane.run_suite` passed the temp directory to pytest rather than explicit file paths.
- pytest only auto-discovers files matching `test_*.py` / `*_test.py`; hidden suite files (`is_prime_hidden.py`, `contracts.py`) do not match → 0 tests collected → all trials scored 0/1 passed.
- Fixed in `src/ahnlab/membrane.py`: now passes explicit copied file paths to pytest instead of the directory.
- Affected: all 18 pilot trials (seeds 1–3, both arms, all subjects). Re-run after fix produced plausible results.

## Deviation 5 — hook path wrong in settings.json

- `PostToolUse` hook command was `python lab/.claude_hooks/log_edit.py`; hook cwd = `lab/` (because `lab/.claude/` makes `lab/` the nested project root for lab files), so path doubled to `lab/lab/.claude_hooks/log_edit.py`.
- Fixed in `.claude/settings.json`: changed to `python .claude_hooks/log_edit.py`. Takes effect next session.
- Impact: telemetry was effectively disabled even when `AHNLAB_TELEMETRY=1` (script not found → exit 1).

## Deviation 6 — hook cwd is file-dependent, not fixed (root cause of Deviations 5–6 confusion)

- Root cause: hook cwd is determined by the nearest `.claude/` directory above the edited file. Files in `lab/` use cwd=`lab/`; files in repo root use cwd=repo root.
- Deviation 5 was therefore correct for lab files but wrong for repo-root files.
- The "revert" in Deviation 6 was based on a repo-root edit error (`AHN\.claude_hooks\`) but should not have been applied globally.
- Final resolution: settings.json uses `python .claude_hooks/log_edit.py` (works from cwd=`lab/` → resolves to `lab/.claude_hooks/log_edit.py`). A stub at `AHN\.claude_hooks\log_edit.py` handles the repo-root case (same command, different cwd → still exits 0).
- Session-cache stubs created at `AHN\.claude_hooks\log_edit.py` and `AHN\lab\lab\.claude_hooks\log_edit.py` for in-flight sessions.
- Fix takes effect next session.

## Deviation 7 — E2 harness extension: per-arm contract files

- E2 requires different contract files per arm (contracts_B.py, contracts_C.py, contracts_D.py). The existing `ArmSpec` only supported `include_contracts: bool` with a glob fallback (`contracts*.py`).
- Extended `ArmSpec` with `contract_filenames: list[str] = []`. If non-empty and `include_contracts=True`, those specific filenames (relative to subject dir) are used instead of the glob. Backward-compatible — E1 arms use empty list and fall back to glob.
- Change in `lab/src/ahnlab/models.py` and `lab/src/ahnlab/arms.py`. Not preceded by a contract on the harness itself (consistent with existing Deviations 2–3).

## Cleanup path

After E1 produces first data, prioritized cleanup:

1. Backfill executable contracts for R1, R5, R6, R7 from existing AEs.
2. Replace single-pass impl with red-green-refactor for any future component.
3. Document the human's independent restatement of intent before E2..E8.
