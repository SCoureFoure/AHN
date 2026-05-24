# E2 Requirements — Contract Completeness

**Experiment ID:** E2  
**Status:** Draft — pending subject selection and hidden-suite sign-off  
**Depends on:** E1 findings (`lab/docs/findings-E1.md`), E1-DIAG-T0 results

---

## 1. Motivation

E1 found that partial contracts (Arm B, `slugify`) increased divergence and reduced pass rate relative to no contracts (Arm A). The finding was attributed to partial spec narrowing the solution space to the wrong region. However, E1-DIAG-T0 (temperature=0 pilot, N=10) showed both arms collapse to identical correct output at temp=0 for `slugify`. This means the model has a strong canonical prior for `slugify` that dominates at low temperature, making the E1 slugify result uninterpretable as a measure of contract completeness: the control arm's "convergence" was the model recalling a canonical implementation, not agents interpreting an intent correctly.

**E2 isolates contract completeness as the independent variable** using a novel synthetic subject where no canonical implementation exists in the model's training distribution.

---

## 2. Research Question

Does contract completeness (fraction of behavioral surface covered by acceptance examples) causally reduce interpretation divergence and increase hidden-suite pass rate?

**Falsification condition:** If Arm D (full contracts) does not achieve lower divergence and higher pass rate than Arms A–C, the hypothesis that completeness drives correctness is not supported by this subject.

---

## 3. Subject Selection Rationale

### Requirements for E2 subject

A valid E2 subject must satisfy:

1. **Not memorized.** At temperature=0, a minimal intent-only prompt must produce divergent outputs across trials — not a single deterministic canonical implementation. (Test: run N=5 at temp=0; if hamming=0.000, the subject fails this criterion.)
2. **Genuine behavioral ambiguity on edge cases.** Multiple reasonable interpretations exist for at least 4 edge cases. Agents will disagree on these without explicit contracts.
3. **Definable complete hidden suite.** A ground-truth correct behavior exists for all edge cases, enabling a hidden suite with known-pass answers.
4. **Small enough to implement in a single function.** Fits in one `solution.py` function. No external dependencies.

### Proposed subject: `normalize_tags`

```text
normalize_tags(tags: list) -> list[str]

Given a list of tag values, return a normalized, deduplicated list of tag strings.
```

**Justification:** This is a data-cleaning task with no canonical implementation. Agents will disagree on:

- Whether to lowercase tags
- Whether to strip leading/trailing whitespace
- What to do with empty strings or whitespace-only strings
- Whether to deduplicate before or after normalization
- What to do with non-string inputs (int, None)
- Whether to preserve input order

The "correct" answers to each ambiguity are not obvious from the function name alone, making this a genuine interpretation test.

**Candidate acceptance examples (hidden suite ground truth — agent never sees these in Arm A/B):**

| input | expected output |
| --- | --- |
| `["Python", "python"]` | `["python"]` (lowercase + dedup) |
| `["  Go  ", "go"]` | `["go"]` (strip + lowercase + dedup) |
| `["", "rust"]` | `["rust"]` (empty strings dropped) |
| `["   "]` | `[]` (whitespace-only dropped) |
| `["   ", "rust"]` | `["rust"]` (whitespace-only dropped; independent of non-str handling) |
| `[None, "go"]` | `["go"]` (None dropped, not cast) |
| `["b", "a", "b"]` | `["b", "a"]` (order-preserving dedup, not sorted) |
| `[]` | `[]` (empty in → empty out) |
| `["Hello World"]` | `["hello world"]` (lowercase, spaces preserved) |

> **Note:** The hidden suite must be finalized before any agent runs. The expected outputs above are the proposed ground truth and must be locked before E2 begins.

**Validation check (required before E2 run):** Run 5 trials of Arm A at temp=0. If all produce identical output → subject is memorized → discard and select alternate. If hamming > 0.000 → proceed.

---

## 4. Arms

E2 varies contract completeness as the independent variable across 4 arms on the same subject.

| Arm | ID | Contracts given to agent | Expected effect |
| --- | --- | --- | --- |
| A | `A_zero` | None (intent only) | High divergence, variable pass rate |
| B | `B_partial` | 2 acceptance examples (basic happy path only) | Lower divergence than A on covered cases; high divergence on uncovered edge cases |
| C | `C_partial_warn` | Same 2 AEs as B + explicit uncertainty warning | Should reduce over-confidence; possibly lower divergence than B on uncovered cases |
| D | `D_full` | All 9 acceptance examples (full coverage) | Minimal divergence; highest pass rate |

### Arm A — Zero contracts (`A_zero`)

Prompt addition: none beyond intent.

### Arm B — Partial contracts (`B_partial`)

Provide exactly 2 acceptance examples as pytest-style contracts:

```python
def test_basic_lowercase():
    assert normalize_tags(["Python", "Go"]) == ["go", "python"]

def test_dedup():
    assert normalize_tags(["rust", "rust"]) == ["rust"]
```

These cover basic lowercase and dedup. They do not cover: empty strings, whitespace-only, non-str inputs, None, internal whitespace, empty input.

### Arm C — Partial + incompleteness warning (`C_partial_warn`)

Same 2 contracts as B, plus the following note prepended to the contracts block:

> **Note:** These acceptance examples cover only the basic cases. The function will be evaluated against additional edge cases not listed here. Implement defensively.

### Arm D — Full contracts (`D_full`)

All 9 acceptance examples from the hidden suite ground truth, encoded as pytest contracts.

---

## 5. Predictions

**Primary prediction (Hypothesis Corollary B test):** Divergence decreases monotonically as completeness increases: `A_zero > B_partial > C_partial_warn > D_full`. Pass rate increases monotonically in same order.

**Secondary prediction:** `C_partial_warn` divergence < `B_partial` divergence. If true, explicit incompleteness acknowledgment partially compensates for missing contracts.

**Falsification condition:** If `A_zero` pass rate ≥ `D_full` pass rate, the novel subject is still memorized and E2 result is invalid. If `B_partial` divergence < `A_zero` divergence, partial contracts over-constrain (E1 `slugify` pattern) — record as Finding.

---

## 6. Hidden Suite

Must be finalized before any runs. The hidden suite encodes the 9 acceptance examples from Section 3. The suite is a superset of Arm D's contracts — same test cases, same expected outputs. Agent never sees the hidden suite.

**Required sign-off:** Human reviews hidden suite expected outputs before run. Any ambiguous expected value (e.g., sort order, None handling) must be explicitly decided and recorded here.

### Decisions — locked 2026-05-24

- [x] `[1, "python"]` test **replaced** by `["   ", "rust"]` → `["rust"]`. Rationale: removes correlation with None test; whitespace-only is an independent dimension.
- [x] `normalize_tags(["b", "a", "b"])` → `["b", "a"]` **(order-preserving dedup)**. Rationale: sort-by-default agents fail in A_zero, converge in D_full — maximizes divergence signal.
- [x] `normalize_tags([None, "go"])` → `["go"]` **(drop None)**. Rationale: consistent drop strategy; avoids `"None"` string as tag output.

---

## 7. Run Parameters

| Parameter | Value |
| --- | --- |
| Model | `claude-haiku-4-5-20251001` |
| Temperature | 0.7 (same as E1 for comparability) |
| Trials per arm | 100 |
| Seeds | 1–100 |
| Total API calls | 400 |
| Estimated cost | ~$0.08–0.12 (Haiku, ~500 in / ~250 out per call) |

---

## 8. Validation Protocol

Before full N=100 run:

1. **Subject memorization check:** 5 trials of `A_zero` at temp=0. Hamming must be > 0.000.
   - **DONE 2026-05-24.** hamming=0.600 at temp=0, N=5. Two distinct pass vectors across 5 seeds. Script: `lab/diagnostics/diag_e2_memcheck.py`, experiment `E2-MEMCHECK-T0`.
   - Failing tests at temp=0: `test_hidden_order_preserving_dedup` (3/5 seeds — agents sort by default) and `test_hidden_none_dropped` (2/5 seeds — agents cast None to `"None"`). Both are exactly the edge cases E2 is designed to resolve with contracts.

2. **Hidden suite lock:** All 3 open decisions in Section 6 resolved. Hidden suite committed and treated as inviolable.
   - **DONE 2026-05-24.** Decisions locked — see Section 6.

3. **Pilot run:** N=10 per arm (~40 calls, ~$0.02) to confirm no harness errors and to preview divergence ordering.

---

## 9. Deliverables

- `lab/experiments/E2/subjects/normalize_tags/intent.md`
- `lab/experiments/E2/subjects/normalize_tags/contracts_B.py` (2 AEs)
- `lab/experiments/E2/subjects/normalize_tags/contracts_C.py` (2 AEs + warning)
- `lab/experiments/E2/subjects/normalize_tags/contracts_D.py` (9 AEs)
- `lab/experiments/E2/hidden/normalize_tags_hidden.py`
- `lab/src/ahnlab/experiments.py` — add `e2_spec()` to REGISTRY
- `lab/docs/findings-E2.md` — post-run findings
