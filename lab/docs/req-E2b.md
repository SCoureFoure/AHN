# E2b/E2c Requirements — C_partial_warn Mechanism + B_partial Inversion Replication

**Experiment IDs:** E2b (group_by_prefix), E2c (invert_index)  
**E2 family:** E2, E2b, E2c all probe contract completeness effects. E2b and E2c were originally numbered E3/E3b but renamed after re-reading lab intent — the original E3 question (multi-cycle regression) is distinct from this E2 completeness extension.  
**Status:** Completed — subject validation failed for both E2b and E2c  
**Depends on:** E2 findings (`lab/docs/findings-E2.md`)

## Outcome note

Both subjects (group_by_prefix, invert_index) failed the A_zero ≤ 0.65 validation criterion — Haiku 4.5 produced A_zero = 1.000 on both. The wrong-default assumption was incorrect for this model/task combination. E2b did replicate the B_partial inversion (1.000 → 0.778) even with correct defaults, which is a real signal. E2c was fully flat (all arms 1.000). Neither subject was valid for RQ1. Held for possible revisit with a different subject class.

---

## 1. Research Questions

**RQ1 — C_partial_warn mechanism:** Is the C_partial_warn advantage in E2 driven by (A) epistemic correction — the warning changes how agents interpret contract completeness — or (B) behavioral triggering — the warning activates defensive defaults that happen to be correct?

To distinguish: use a subject where agents have **wrong** defaults, not correct ones. If C_partial_warn still outperforms A_zero → mechanism A. If C_partial_warn fails to help → mechanism B, and E2's finding is fragile (limited to tasks with recognizable defensive patterns).

**RQ2 — B_partial inversion robustness:** E1 and E2 both show partial contracts reducing pass rate below no contracts. E2 attributed this to partial contracts suppressing correct defaults. Does the inversion hold when agent defaults are wrong? If yes → inversion is about false completeness signal (universal). If no → inversion was specific to suppressed correct priors.

---

## 2. Subject Requirements

A valid E3 subject must satisfy all of:

1. **Wrong agent defaults.** At temp=0.7, A_zero pass rate must be materially lower than E2's A_zero baseline (0.833). Target: A_zero hidden pass rate ≤ 0.65. If agents get most things right by default, E3 cannot answer RQ1.
2. **Not memorized.** At temp=0, A_zero hamming > 0.000.
3. **Definable ground truth.** A complete hidden suite with known-correct behaviors.
4. **Single function, no external dependencies.**

---

## 3. Proposed Subject: `group_by_prefix`

```text
group_by_prefix(items: list[str], sep: str) -> dict[str, list[str]]

Given a list of strings and a separator, group items by their prefix
(the text before the first occurrence of sep). Return a dict mapping
each prefix to a list of suffixes in insertion order.
```

**Why this subject:** The "obvious" implementation skips or mishandles items that contain no separator. Items without `sep` are non-obvious — do you skip them, include them with an empty suffix, or raise? The answer (include with `""` suffix) is not the agent's default. This creates a systematic wrong-default that is independent of "defensive programming" habits.

### Hidden suite ground truth (9 tests) — locked

| input | sep | expected output |
| --- | --- | --- |
| `["a.x", "b.y"]` | `"."` | `{"a": ["x"], "b": ["y"]}` |
| `["a.x", "a.y"]` | `"."` | `{"a": ["x", "y"]}` |
| `["a.x", "tag"]` | `"."` | `{"a": ["x"], "tag": [""]}` |
| `["tag"]` | `"."` | `{"tag": [""]}` |
| `["x.y.z"]` | `"."` | `{"x": ["y.z"]}` (split on first sep only) |
| `[]` | `"."` | `{}` |
| `["a.x", "a.x"]` | `"."` | `{"a": ["x", "x"]}` (duplicates preserved) |
| `["b.2", "a.1"]` | `"."` | `{"b": ["2"], "a": ["1"]}` (insertion order, not sorted) |
| `[".x"]` | `"."` | `{"": ["x"]}` (empty prefix is valid) |

### Open decisions — locked

- Items with no separator → include with `""` suffix (not skip, not raise)
- Multiple separators in one item → split on first only, remainder is the suffix
- Insertion order preserved for both keys and values
- Duplicate items → preserved (not deduplicated)

**Expected wrong-default tests:** Tests 3, 4, 9 are the primary wrong-default tests. Agents will skip no-sep items (tests 3/4) and handle empty-prefix items incorrectly (test 9). These are NOT the kind of edge cases that "implement defensively" triggers — agents have no "data cleaning" analog here.

---

## 4. Arms

| Arm | ID | Contracts | Purpose |
| --- | --- | --- | --- |
| A | `A_zero` | None | Baseline with wrong defaults |
| B | `B_partial` | 2 basic AEs (happy path only) | Does inversion persist with wrong defaults? |
| C | `C_partial_warn` | 2 AEs + incompleteness warning | Does warning help when defaults are wrong? |
| D | `D_full` | All 9 AEs | Confirms contracts can overcome wrong defaults |

### Arm B contracts (`contracts_B.py`)

```python
from solution import group_by_prefix

def test_basic():
    assert group_by_prefix(["a.x", "b.y"], ".") == {"a": ["x"], "b": ["y"]}

def test_multiple_values_same_prefix():
    assert group_by_prefix(["a.x", "a.y"], ".") == {"a": ["x", "y"]}
```

These do NOT cover: no-separator items, multi-separator items, empty prefix, empty list, duplicates, insertion order of keys.

### Arm C contracts (`contracts_C.py`)

Same 2 contracts as B plus:

```
# NOTE: These contracts cover only the basic cases.
# The function will be evaluated against additional edge cases not listed here.
# Implement defensively.
```

### Arm D contracts (`contracts_D.py`)

All 9 acceptance examples from the hidden suite ground truth.

---

## 5. Predictions

**Primary (RQ1):** If mechanism A — C_partial_warn pass rate > A_zero pass rate with this subject. If mechanism B — C_partial_warn pass rate ≈ A_zero pass rate (warning triggers no useful defaults).

**Secondary (RQ2):** If inversion is universal — B_partial pass rate < A_zero pass rate (partial contracts still worse than no contracts). If inversion was prior-specific — B_partial pass rate ≥ A_zero pass rate (no correct priors to suppress, contracts can only help or be neutral).

**Baseline prediction:** D_full pass rate ≥ 0.95. Full contracts should overcome wrong defaults.

**Divergence prediction:** D_full hamming = 0.000 (replicates E2). A_zero hamming > E2 A_zero (0.765) — more disagreement expected when agents have wrong and varied defaults.

---

## 6. Run Parameters

| Parameter | Value |
| --- | --- |
| Model | `claude-haiku-4-5-20251001` |
| Temperature | 0.7 |
| Trials per arm | 100 |
| Seeds | 1–100 |
| Total API calls | 400 |
| Estimated cost | ~$0.50–0.55 |

---

## 7. Validation Protocol (run before full N=100)

1. **Memorization check:** 5 trials `A_zero` at temp=0. Hamming must be > 0.000. Script: adapt `lab/diagnostics/diag_e2_memcheck.py` for E3.
2. **Wrong-default check:** 10 trials `A_zero` at temp=0.7. Hidden pass rate must be ≤ 0.65. If pass rate is too high (agents get defaults right), subject is invalid for E3 — select alternate.
3. **Hidden suite lock:** All decisions above treated as inviolable from this point.
4. **Pilot run:** N=10 per arm (~40 calls, ~$0.05) to confirm harness and preview divergence ordering.

---

## 8. Alternate Subject (if `group_by_prefix` fails validation)

**`invert_index(pairs)`** — given a list of `(key, value)` tuples, return a dict mapping each value to the list of keys that produced it, in insertion order. Edge cases: duplicate `(key, value)` pairs (include or deduplicate?), None values, empty list. Agents will likely dedup by default; spec preserves duplicates.

---

## 9. Deliverables

- `lab/experiments/E3/subjects/group_by_prefix/intent.md`
- `lab/experiments/E3/subjects/group_by_prefix/contracts_B.py`
- `lab/experiments/E3/subjects/group_by_prefix/contracts_C.py`
- `lab/experiments/E3/subjects/group_by_prefix/contracts_D.py`
- `lab/experiments/E3/hidden/group_by_prefix_hidden.py`
- `lab/src/ahnlab/experiments.py` — add `e3_spec()` to REGISTRY
- `lab/docs/findings-E3.md` — post-run
