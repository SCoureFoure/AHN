# E2 Findings — Contract Completeness

**Run date:** 2026-05-24  
**Trials:** 50 per arm. Model: `claude-haiku-4-5-20251001`. Subject: `normalize_tags`.  
**Total cost:** $0.26

---

## Summary of Results

| arm | n | hamming | hidden pass rate | cost $ |
| --- | --- | --- | --- | --- |
| A_zero | 50 | 0.765 | 0.833 | 0.0619 |
| B_partial | 50 | 0.549 | 0.371 | 0.0471 |
| C_partial_warn | 50 | 0.350 | 0.913 | 0.0691 |
| D_full | 50 | 0.000 | 1.000 | 0.0803 |

### Per-test failure counts by arm

| test | A_zero | B_partial | C_partial_warn | D_full |
| --- | --- | --- | --- | --- |
| `test_hidden_none_dropped` | 38/50 | 48/50 | 0/50 | 0/50 |
| `test_hidden_order_preserving_dedup` | 37/50 | 37/50 | 39/50 | 0/50 |
| `test_hidden_strip_and_dedup` | 0/50 | 50/50 | 0/50 | 0/50 |
| `test_hidden_whitespace_only_dropped` | 0/50 | 50/50 | 0/50 | 0/50 |
| `test_hidden_whitespace_only_in_mixed_list` | 0/50 | 50/50 | 0/50 | 0/50 |
| `test_hidden_empty_string_dropped` | 0/50 | 48/50 | 0/50 | 0/50 |

---

## Finding 1 — Divergence decreases monotonically with completeness (primary prediction confirmed)

Hamming order: `A_zero (0.765) > B_partial (0.549) > C_partial_warn (0.350) > D_full (0.000)`.

The primary prediction was fully confirmed. D_full achieves zero divergence and 1.000 pass rate. Every agent given complete contracts produced identical correct output.

---

## Finding 2 — Partial contracts (B_partial) simultaneously reduce divergence and catastrophically reduce pass rate

B_partial hamming (0.549) is lower than A_zero (0.765) — contracts reduced divergence as predicted. But B_partial pass rate (0.371) is dramatically lower than A_zero (0.833). Partial contracts made correctness *worse* by 46 percentage points.

**Mechanism — false completeness signal:** The two B_partial contracts test `["Python", "Go"] → ["python", "go"]` (lowercase) and `["rust", "rust"] → ["rust"]` (dedup). Neither input requires stripping — `"Python"` → `"python"` passes with or without a strip step. Agents that implement *exactly what the contracts encode* — lowercase and dedup, no strip — are correct for all contracted inputs but wrong for hidden suite inputs that require stripping.

The per-test breakdown proves this: B_partial produces 50/50 failures on `strip_and_dedup`, `whitespace_only_dropped`, and `whitespace_only_in_mixed_list` — tests that require strip behavior. A_zero produces 0/50 failures on all three. Agents without contracts default to rich defensive implementations including stripping. Agents with partial contracts implement the minimum that satisfies those contracts. If strip is not in the contracts, strip is not in the implementation.

**The partial spec is not neutral — it actively misleads.** The agent correctly reads the contracts as a complete specification. The absence of stripping in the contracts signals "stripping is not required." This is technically accurate for the contracted inputs, but false for the hidden suite.

This replicates and extends E1's `slugify` finding (E1 Finding 1). In E1, we attributed the inversion to "prior training on canonical implementations." In E2, with a synthetic novel subject, the mechanism is confirmed as a genuine spec interpretation effect, not prior recall.

---

## Finding 3 — Incompleteness warning (C_partial_warn) recovers pass rate while reducing divergence below A_zero

C_partial_warn achieves hamming 0.350 and pass rate 0.913. Compared to both other incomplete arms:

- vs A_zero: lower divergence (0.350 vs 0.765) **and** higher pass rate (0.913 vs 0.833)
- vs B_partial: lower divergence (0.350 vs 0.549) **and** dramatically higher pass rate (0.913 vs 0.371)

The warning text — *"These contracts cover only the basic cases. The function will be evaluated against additional edge cases not listed here. Implement defensively."* — broke the false completeness signal. Agents receiving the warning reverted to defensive implementations that include stripping and None-dropping, while still benefiting from the 2 explicit contracts to converge on lowercase and dedup.

C_partial_warn is the only arm that outperforms A_zero on both dimensions simultaneously. This is not predicted by a simple "more contracts → better" model. The value is not the additional information (there is none — same 2 contracts as B_partial) but the *epistemic signal*: explicit acknowledgment that the spec is incomplete changes how agents interpret the contracts.

**One persistent failure:** `order_preserving_dedup` fails at 39/50 in C_partial_warn (and 37/50 in A_zero, 37/50 in B_partial). The warning prompts defensive implementations but cannot resolve order ambiguity — agents default to sorted output because "clean, consistent tags" does not signal insertion-order preservation. Only D_full, which explicitly contracts `["b", "a", "b"] → ["b", "a"]`, resolves this.

---

## Finding 4 — Agent defaults are rich but sort-biased

In A_zero (no contracts, no warning), agents produce implementations that:
- Strip whitespace: **pass 50/50** on all whitespace tests
- Drop empty strings: **pass 50/50**
- Lowercase: **pass 50/50** (implied by hamming > 0)
- Drop None: fail 38/50 — agents cast `None → "None"` by default
- Preserve insertion order: fail 37/50 — agents sort by default

The "canonical normalize_tags" in agent training data appears to include stripping and lowercasing but is ambiguous on None handling (~24% drop, ~76% cast) and sort order (~26% preserve, ~74% sort).

This baseline profile explains B_partial's disaster: B_partial takes a richly correct baseline implementation and *removes* the strip behavior by providing contracts that don't require it.

---

## Implications for the AHN Framework

**Corollary B confirmed (with a new mechanism):** Contract quality determines outcome, not agent capability. Agents are capable of producing correct `normalize_tags` implementations — A_zero demonstrates this (pass rate 0.833 despite zero contracts). The degradation in B_partial is entirely attributable to the false completeness signal from incomplete contracts, not to agent incapability.

**New implication — contract incompleteness must be acknowledged:** A partial spec that is presented as complete is worse than no spec on tasks where agents have strong, correct priors. The correct pattern for incremental specification is either (a) explicitly mark specs as incomplete (C_partial_warn pattern) or (b) ensure the partial spec covers all the behaviors agents would otherwise default to incorrectly. Incompleteness that silences correct defaults is an anti-pattern.

**Open question for E3:** The C_partial_warn advantage is driven by the warning text triggering defensive defaults. Would this hold for a subject where agents do NOT have defensible priors — i.e., a purely novel task where there is no "implement defensively" fallback? The warning may only work when agent training includes recognizable "data cleaning" patterns. This hypothesis distinguishes two mechanisms: (1) the warning corrects interpretation of contract completeness, or (2) the warning triggers defensive defaults that happen to be correct. E3 should use a subject where agent defaults are incorrect to distinguish these.

---

## Remaining open questions

1. **Is the B_partial inversion generalizable?** E1 and E2 both show partial contracts reducing pass rate. The mechanism differs slightly (E1: canonical recall suppressed; E2: strip behavior suppressed by false completeness signal). A third replication with a different subject type would strengthen the claim.

2. **N=50 robustness.** Increase to N=100 to confirm C_partial_warn pass rate stability (0.913 at N=50 could shift).

3. **C_partial_warn mechanism.** The warning text as written is fairly explicit. Test weaker warnings ("additional cases may exist") and stronger ones ("you will be graded on behaviors not listed here"). How specific does the signal need to be?
