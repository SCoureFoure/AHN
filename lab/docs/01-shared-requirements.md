# AHN Lab — Shared Requirements

Cross-cutting components used by all experiments (E1..E8). Each component carries acceptance examples that drive its contracts.

---

## R1. Task Harness

**Responsibility:** Load a task definition, spawn an agent session against the Anthropic Messages API, capture transcript, tool calls, artifacts, and cost into a run record.

**Inputs:** `TaskSpec` (intent text, optional contracts, optional pre-existing artifacts, model id, max tokens, system prompt, tool defs).
**Outputs:** `RunRecord` (run_id, task_id, model, started_at, ended_at, input_tokens, output_tokens, cost_usd, transcript jsonl path, artifacts dir, terminal status).

**Acceptance examples:**

- **AE-R1-1:** Given `TaskSpec(intent="Return the string 'hello'", model="claude-haiku-4-5-20251001", max_tokens=200)`, harness produces a `RunRecord` with `terminal_status="ok"`, non-empty transcript, and `output_tokens > 0`.
- **AE-R1-2:** Given a `TaskSpec` referencing a missing model id, harness produces a `RunRecord` with `terminal_status="api_error"` and an error reason string. It must not raise.
- **AE-R1-3:** Two consecutive runs of the same `TaskSpec` produce two distinct `run_id`s and two distinct transcript files; neither overwrites the other.

---

## R2. Membrane Runner

**Responsibility:** Execute programmatic contracts (pytest) against an agent-produced artifact set and return a structured pass/fail report.

**Inputs:** path to artifact dir, path to contract suite (pytest).
**Outputs:** `MembraneReport` (per-test name, status, duration, failure message if any, summary counts).

**Acceptance examples:**

- **AE-R2-1:** Given an artifact dir whose code satisfies all contracts, `MembraneReport.failures == 0` and `report.passed == report.total`.
- **AE-R2-2:** Given an artifact dir missing the expected entrypoint module, runner reports a collection error rather than crashing, and every contract reports `status="error"`.
- **AE-R2-3:** Runner times out individual contracts at a configured per-test budget (default 10s) and reports `status="timeout"` for the offender, allowing other contracts to continue.

---

## R3. Judge Pool

**Responsibility:** Run LLM-graded rubrics against an artifact set with multiple judge models and prompt perturbations, return per-judge scores and aggregate inter-rater statistics.

**Inputs:** artifact dir, `RubricSpec` (criterion text, scale, anchor descriptions per scale point), list of judge model ids, perturbation count.
**Outputs:** `RubricReport` (per-judge per-perturbation score, mean, stdev, Krippendorff alpha or analog).

**Acceptance examples:**

- **AE-R3-1:** Given a `RubricSpec` with a 1-5 scale and 3 judges × 2 perturbations on a single artifact, report contains 6 scores plus aggregates.
- **AE-R3-2:** Rubric prompts must include the anchor descriptions verbatim for every score point. Missing anchors must cause `RubricSpec` validation to fail before any API call.
- **AE-R3-3:** When all 6 scores equal the same value, reported stdev is 0 and reported agreement metric is at its maximum.

---

## R4. Results Store

**Responsibility:** Persist `RunRecord`, `MembraneReport`, `RubricReport` rows in DuckDB. Support arm tagging and experiment grouping.

**Inputs:** record objects, experiment_id, arm_id.
**Outputs:** rows in `runs`, `membrane_reports`, `rubric_reports`, `experiments`, `arms` tables. Foreign keys preserved.

**Acceptance examples:**

- **AE-R4-1:** Inserting the same `run_id` twice must raise a uniqueness violation; idempotent inserts must use an explicit upsert API.
- **AE-R4-2:** Querying `SELECT count(*) FROM runs WHERE experiment_id = ? AND arm_id = ?` returns the exact count of runs persisted for that (experiment, arm) pair.
- **AE-R4-3:** Store schema is created idempotently on connect — repeated startup against an existing DB must not error or alter data.

---

## R5. Arm Controller

**Responsibility:** Given an experiment definition with N arms, run K trials per arm with matched seeds and models, write all results tagged with experiment_id and arm_id.

**Inputs:** `ExperimentSpec` (id, description, arms, trials_per_arm, shared seed schedule).
**Outputs:** populated rows in the results store plus a manifest jsonl of every run executed.

**Acceptance examples:**

- **AE-R5-1:** Two arms, 5 trials each, shared seed schedule `[1..5]`: every seed appears in both arms exactly once.
- **AE-R5-2:** A failure in one trial of one arm must not prevent the remaining trials in either arm from executing.
- **AE-R5-3:** Re-running the same `ExperimentSpec` after partial completion resumes from the unfinished trials rather than duplicating completed ones.

---

## R6. Cost & Reproducibility Capture

**Responsibility:** Every `RunRecord` carries enough metadata that another operator can reproduce the run within a tolerance: model id, model version pin if available, prompt hash, seed, lab git SHA, dependency lockfile hash, env var fingerprint (non-secret), API request id.

**Acceptance examples:**

- **AE-R6-1:** Given a `RunRecord`, the lab CLI can print a reproduction command that, run on the same git SHA with the same lockfile, will hit the same prompt hash.
- **AE-R6-2:** API request id from the response header is persisted on every `RunRecord` where the request reached the API.
- **AE-R6-3:** Cost is computed from `input_tokens` and `output_tokens` against a versioned price table; the price table version is recorded on the run.

---

## R7. CLI

**Responsibility:** Single entrypoint `ahnlab` with subcommands: `run`, `report`, `list-experiments`, `init`, `reproduce`.

**Acceptance examples:**

- **AE-R7-1:** `ahnlab run --experiment E1` executes the E1 spec and exits non-zero if any arm fails to complete its configured trial count.
- **AE-R7-2:** `ahnlab report --experiment E1` prints a table of per-arm aggregates (count, mean primary metric, stdev) to stdout.
- **AE-R7-3:** `ahnlab init` creates the DuckDB file and schema if missing; running it against an existing valid DB is a no-op exit 0.

---

## Bootstrap exceptions

The following requirements deviate from the framework's "intent originates from human" rule because they were co-drafted with an agent for velocity:

- All of R1..R7 above were drafted in conversation between the human and the agent. The acceptance examples were proposed by the agent and accepted by the human without independent restatement.
- This exception is recorded here and will be revisited once the lab is producing data.
