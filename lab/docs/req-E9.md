# E9 — Config Impact on Agent Productivity (Meta-experiment)

**Hypothesis target:** The framework's central structural claim, applied recursively to agent tooling. If AHN-style configuration (explicit intent in CLAUDE.md, path-scoped rules acting as contracts, restricted subagent tools acting as enforcement) produces measurably better agent outcomes than ad-hoc configuration, that supports CorB (the membrane is the leverage point) extended to the meta-level. If not, the .claude theatre is overhead.

**Claim under test:** Two `.claude` configurations — one AHN-structured, one minimal/ad-hoc — applied to identical tasks will produce measurably different outcomes on cost, edits-to-green, and contract-violation rate.

---

## Design

Two arms × N tasks per arm × matched seeds.

| Arm | `.claude/` configuration |
|---|---|
| A (ad-hoc) | Empty `.claude/settings.json` with no permissions, no CLAUDE.md, no rules, no skills, no subagents. Single allow-list line for `Bash(*)`. Pure baseline. |
| B (AHN-structured) | Full config as designed in `.claude/ARCHITECTURE.md`: scoped CLAUDE.md, path-scoped rules, skills, subagents, hooks. |

Both arms run against the same task set, headed by the same human prompt, with matched random seeds where stochasticity is present.

---

## Task set (TODO(human) — needs initial seed list)

Each task is a self-contained engineering ask with an objective measurement of done. Candidates:

1. Add a new acceptance example to an existing experiment's req file and propagate it to contracts + hidden suite.
2. Backfill executable contracts for one of R1, R5, R6, R7 from `lab/docs/01-shared-requirements.md`.
3. Add a new subject to E1 with intent, contracts, and hidden suite.
4. Implement a new CLI subcommand `ahnlab inspect <run-id>` that prints transcript path and membrane reports.

The first three are concrete; the fourth has a clean acceptance criterion. The human must lock the final task list before running.

---

## Metrics

**Primary — edits-to-green:** Number of file edits between task start and `pytest tests/lab -q` passing. Lower is better.

**Predicted result:** Arm B mean edits-to-green strictly less than Arm A on tasks 1, 2, 3 (work that benefits from scoped vocabulary and lab CLAUDE.md). Possibly no difference on task 4 (simple addition).

**Secondary metrics:**
- Total cost per completed task
- Number of contract violations (existing tests broken) during the work
- Whether the task completed at all within a 30-edit budget
- Cache hit ratio averaged over the task

---

## Falsifiers for E9 specifically

- If Arm B edits-to-green is greater than or equal to Arm A across all tasks, the AHN-structured config is not paying for itself in this scope.
- If contract violations are equal or higher in Arm B, the rules/subagents are not constraining behavior as designed.
- If the cost delta is negligible (within 20% across arms), the config has no economic justification at the measured scale.

---

## Telemetry requirement

E9 requires `AHNLAB_TELEMETRY=1` to be set during all trials. The PostToolUse hook produces the per-edit data that drives edits-to-green. The SessionStart hook captures the config snapshot used.

Note this dependency in the experiment's runbook before any trial begins.

---

## Acceptance examples for the E9 runner code itself

- AE-E9-R-1: `ahnlab run --experiment E9` requires `AHNLAB_TELEMETRY=1` to be set; otherwise exits non-zero with a clear error.
- AE-E9-R-2: Running each arm requires swapping `.claude/` config — the runner must snapshot the existing config, swap, run, restore. Failure to restore must be loud.
- AE-E9-R-3: `ahnlab report --experiment E9` reports edits-to-green, cost, violations, and budget breach rate per (arm, task).

---

## Status

**Specification only.** E9 is not implementable until E1 produces baseline data and at least one of E2, E3 is also live. Without other experiments running, the meta-experiment has no productivity baseline.

The instrumentation hooks needed (PostToolUse, SessionStart) are already in place opt-in via `AHNLAB_TELEMETRY=1`. Schemas in `lab/runs/claude_telemetry.duckdb` are created on first telemetry-enabled session.
