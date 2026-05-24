# E1 Findings — Interpretation Variance

**Run date:** 2026-05-24
**Trials:** 30 per arm per subject (seeds 4–30). Model: `claude-haiku-4-5-20251001`.
**Full report snapshot:** `lab/runs/reports/E1-20260524-144154.md`

---

## Summary of Results

| subject | arm | hamming | hidden pass rate |
| --- | --- | --- | --- |
| is_prime | A_control | 0.000 | 0.889 |
| is_prime | B_contracts | 0.000 | 0.889 |
| slugify | A_control | 0.067 | 0.996 |
| slugify | B_contracts | 1.395 | 0.893 |
| summarize | A_control | 0.129 | 0.990 |
| summarize | B_contracts | 0.000 | 1.000 |

---

## Finding 1 — Partial contracts increase divergence and decrease pass rate on uncovered edge cases

The prediction (Arm A divergence ≫ Arm B divergence on subjects 2 and 3) was **partially falsified**. `summarize` matched the prediction. `slugify` inverted it.

**Mechanism:** The `slugify` contracts encoded 3 acceptance examples — `hello-world`, `trim-me`, `multi---dash`. All three are basic happy-path cases. The hidden suite contains 9 tests, including edge cases not represented in the contracts: leading/trailing punctuation (`--hello--`), all-punctuation input (`!!!`), unicode (`Café`), empty string, underscores, numeric.

Arm B solutions satisfied the 3 contracts minimally. Implementations diverged on whether they included: unicode normalization, leading/trailing hyphen stripping, non-alnum removal. The contracts did not require these behaviors, so agents did not consistently produce them.

Arm A solutions, given no constraints, converged on the canonical "full" slugify pattern (NFKD normalize → ASCII encode → lower → strip non-alnum → collapse hyphens → strip edges) in 29 of 30 trials. This is the pattern that satisfies all 9 hidden tests. Without a partial spec, agents reached for the robust standard implementation.

**Conclusion:** Partial contracts gave agents a false signal that the specification was complete. Agents implemented the minimum required by the contracts. The unconstrained arm converged on a richer, more correct implementation by defaulting to prior training on canonical implementations of the same task.

---

## Finding 2 — Low-ambiguity subjects are insensitive to treatment

`is_prime` produced identical divergence (0.000) and identical pass rates (0.889) in both arms. Every trial in both arms produced the same pass/fail vector. The single consistently failing hidden test is likely the same edge case across all trials (probable candidate: `is_prime` on non-integer input or negative numbers).

This matches the prediction (convergence on Subject 1). It also confirms that for fully-specified mathematical functions, the treatment has no leverage — the task space is already fully determined by the problem statement.

---

## Finding 3 — Contracts helped on summarize

`summarize` matched the prediction: B_contracts divergence collapsed to 0.000 with pass rate 1.000, compared to A_control divergence 0.129 and pass rate 0.990. The `summarize` contracts encode non-obvious behaviors (missing `qty` defaults to 1; empty list returns specific structure). For subjects where the correct behavior is genuinely ambiguous and the contracts encode that ambiguity resolution, treatment worked as predicted.

The contrast between `slugify` (Finding 1) and `summarize` (this finding) suggests the treatment is most effective when: (a) the task has genuine behavioral ambiguity that the contracts resolve, and (b) the contracts cover the ambiguity rather than only the happy path.

---

## Implication for E2 Design

E1 reveals a contract quality dimension that the original design did not isolate: **contract completeness relative to the hidden suite**. The `slugify` failure is attributable to partial contracts, not to the absence of contracts. This suggests an additional arm or subject dimension for E2:

- **Arm C — complete contracts:** All hidden-suite behaviors encoded as contracts, including edge cases. Compare Arm B (partial contracts) and Arm C (complete contracts) on the same subjects and hidden suite. If Arm C divergence collapses and pass rate matches Arm A's floor, the completeness hypothesis is confirmed.

- **Alternative framing:** E2 could hold subject constant and vary contract completeness as the independent variable: 0 contracts, partial contracts (3 AEs), full contracts (all AEs), over-specified contracts (AEs + implementation hints). This would directly measure the relationship between contract coverage and divergence.

The `slugify` result is also consistent with Corollary B of the framework hypothesis: the bottleneck is not agent capability but contract quality. Arm A's strong performance on `slugify` is not because A_control agents are more capable — it is because the absence of a partial spec allowed agents to apply their full prior training on canonical implementations. The partial spec in Arm B was a constraint that narrowed the solution space to the wrong region.

---

## Diagnostics Run (2026-05-24)

### Diagnostic 1 — `is_prime` hidden test audit

**Test failing in every trial:** `test_hidden_is_prime_typeerror_on_float`

```text
is_prime(3.0) — expected: raises TypeError or ValueError
               actual: returns True (no exception)
```

**Root cause:** A requirement gap. The `is_prime` intent.md and contracts are silent on float input. No agent produced a type check. This is not an agent failure — it is a missing contract. The hidden suite encodes a behavior that was never specified above it.

**Verdict:** The hidden suite contains a test for which no requirement exists. This is a contract-above-hidden-suite consistency failure in the lab's own setup. For E2, hidden suite tests must trace to a requirement decision (recorded in req-EN.md) before being locked.

### Diagnostic 2 — Temperature confound pilot (slugify, N=10, temp=0)

Stored as experiment `E1-DIAG-T0`. Script: `lab/diagnostics/diag_temp0_slugify.py`.

| arm | n | hamming (temp=0) | pass rate (temp=0) | hamming (E1, temp=0.7) | pass rate (E1, temp=0.7) |
| --- | --- | --- | --- | --- | --- |
| A_control | 10 | **0.000** | **1.000** | 0.067 | 0.996 |
| B_contracts | 10 | **0.000** | **1.000** | 1.395 | 0.893 |

Both arms collapse to identical correct output at temp=0. At temp=0, B_contracts also achieves 9/9 pass rate — the model's canonical `slugify` prior overrides the partial spec constraint when sampling is deterministic.

**Verdict:** `slugify` is memorized. The E1 A_control convergence signal is dominated by the model recalling a canonical implementation, not agents converging through interpretation. The E1 B_contracts divergence at temp=0.7 was the partial spec disrupting the canonical recall path, causing stochastic exploration of a narrower (wrong) solution space.

**Implication for E2:** E2 must use a synthetic novel subject where the model has no canonical prior. Validation protocol: 5 temp=0 trials of the no-contract arm; hamming must be > 0.000 before the subject is approved.

## Remaining open questions

1. **Is `summarize` finding robust?** 30 trials is not large. Re-run `summarize` at N=100 to confirm the 0.000 hamming result holds.
