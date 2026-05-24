# E1 — Interpretation Variance

**Hypothesis target:** CorA (top-down spec sans contracts → misalignment) and A4 (prose interpretation diverges across sessions).

**Claim under test:** When N fresh agent sessions are given the same natural-language requirement *without* contracts, their outputs diverge significantly. When given the same requirement *with* failing acceptance tests, divergence collapses toward zero.

---

## Design

Two arms × N trials per arm × same task spec, except for presence of contracts.

| Arm | Inputs given to agent |
|---|---|
| A (control) | Intent text only. No tests. |
| B (treatment) | Intent text + a pre-existing failing pytest suite that encodes the acceptance examples. |

Both arms produce a single Python module satisfying the request. Both arms are scored by a *hidden* judge suite that the agent never sees — the same hidden suite for both arms. Divergence is measured across trials within each arm.

**N (trials per arm):** 30 to start. Power calculation deferred until pilot variance is observed.

**Model:** `claude-haiku-4-5-20251001` (cheap, fast, sufficient for divergence signal). Repeat with `claude-sonnet-4-6` if pilot shows Haiku saturates at floor or ceiling.

---

## Subjects

Three synthetic kata tasks of escalating ambiguity:

1. **Low-ambiguity:** "Write a function `is_prime(n: int) -> bool` that returns True iff n is prime."
2. **Mid-ambiguity:** "Write a function `slugify(s: str) -> str` that converts a string into a URL slug."
3. **High-ambiguity:** "Write a function `summarize(items: list[dict]) -> dict` that summarizes a list of order items."

For each subject, the contract suite for Arm B encodes the acceptance examples below. The hidden judge suite is a superset, including edge cases the contract suite does not state.

---

## Acceptance examples (these become Arm B's contracts AND seed the hidden judge suite)

**Subject 1 — is_prime**

- AE-E1-1.1: `is_prime(2) == True`
- AE-E1-1.2: `is_prime(4) == False`
- AE-E1-1.3: `is_prime(1) == False`
- AE-E1-1.4: `is_prime(0) == False`

Hidden suite adds: negatives, large primes, type errors on non-int.

**Subject 2 — slugify**

- AE-E1-2.1: `slugify("Hello World") == "hello-world"`
- AE-E1-2.2: `slugify("  Trim Me  ") == "trim-me"`
- AE-E1-2.3: `slugify("multi---dash") == "multi-dash"`

Hidden suite adds: unicode, leading/trailing punctuation, empty string, all-punctuation input.

**Subject 3 — summarize**

- AE-E1-3.1: Empty list → `{"count": 0, "total": 0.0}`.
- AE-E1-3.2: `[{"price": 1.0, "qty": 2}, {"price": 3.0, "qty": 1}]` → `{"count": 2, "total": 5.0}`.
- AE-E1-3.3: Item missing `qty` is treated as `qty=1`.

Hidden suite adds: items with missing `price` (the requirement is silent — treat as exception), negative prices, mixed currencies (out of scope, must not be invented), very large lists.

---

## Metrics

**Primary metric — output divergence per arm:**

For each trial output, run the hidden judge suite and record the pass/fail vector (length = number of hidden tests). Divergence within an arm = mean pairwise Hamming distance across pass/fail vectors across the N trials.

**Predicted result:**
- Arm A divergence ≫ Arm B divergence on Subjects 2 and 3.
- Arm A and Arm B divergence may converge on Subject 1 (low ambiguity).

**Secondary metrics:**
- Mean hidden-suite pass rate per arm per subject (raw correctness).
- AST similarity across trials within arm (structural divergence proxy).
- Tokens spent per arm per subject (cost-of-correctness signal).

---

## Falsifiers for E1 specifically

- If Arm A divergence ≤ Arm B divergence on Subjects 2 and 3, the prediction is falsified.
- If Arm B hidden-suite pass rate is not strictly greater than Arm A on at least Subjects 2 and 3, the claim that contracts pull behavior toward intent is weakened.
- If divergence in either arm is dominated by API non-determinism rather than interpretation (testable by setting `temperature=0` and measuring residual variance), the metric must be reformulated.

---

## Acceptance examples for the E1 runner code itself

- AE-E1-R-1: `ahnlab run --experiment E1` produces 2 × N × 3 = 180 rows in `runs` table at default N=30.
- AE-E1-R-2: `ahnlab report --experiment E1` prints divergence per (arm, subject) and a delta column.
- AE-E1-R-3: If the contract suite for Arm B is malformed (cannot be collected by pytest), the experiment refuses to start rather than running Arm A only.
