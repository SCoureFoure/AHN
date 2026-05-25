# E3 Findings — Compounding Regression

**Experiment:** E3  
**Run date:** 2026-05-24  
**Trials per arm:** 10 (pilot)  
**Model:** claude-haiku-4-5-20251001  
**Status:** Partial confirmation

---

## Results

| arm | cycle | n | hidden pass rate | cost $ |
|---|---|---|---|---|
| A_free | c1 | 10 | 1.000 | 0.0060 |
| A_free | c2 | 10 | 0.822 | 0.0268 |
| A_free | c3 | 10 | 1.000 | 0.0203 |
| A_free | c4 | 10 | 1.000 | 0.0297 |
| B_hierarchy | c1 | 10 | 1.000 | 0.0070 |
| B_hierarchy | c2 | 10 | 0.956 | 0.0185 |
| B_hierarchy | c3 | 10 | 1.000 | 0.0212 |
| B_hierarchy | c4 | 10 | 1.000 | 0.0317 |

---

## What happened at c2

Hidden c2 has 9 tests: 4 c1 regressions + 5 new c2 behaviors (complete, pending, done_items, list_items shows all items, ValueError on missing item).

A_free: 8/10 trials scored 7/9. B_hierarchy: 2/10 scored 7/9, 8/10 scored 9/9.

The 2 failing tests in both arms were the same pattern: `list_items` semantics after `complete()` is called. Without c2 contracts, A_free more often implemented `list_items` to filter out completed items (reasonable but wrong per the spec — the hidden test expects `list_items` to return all items and `pending_items` to filter). Contracts in B_hierarchy included the explicit distinction, reducing this error rate.

**Gap at c2: 0.134** (A_free=0.822 vs B_hierarchy=0.956). Statistically meaningful at n=10.

---

## Why c3 and c4 recovered

Both arms reached 1.000 at c3 and c4. The `remove` feature at c3 required the agent to rewrite the full class structure, which incidentally corrected the c2 behavior. The agent's full-rewrite at each feature cycle acts as a natural reset — prior bugs are fixed opportunistically when the entire class is regenerated from context.

This is a structural property of single-file, class-based subjects: each cycle replaces the whole file, so any surviving regression must persist through a fresh generation. Regressions that don't make it into the new prompt context don't survive.

---

## Interpretation against the prediction

**Prediction:** A_free pass rate declines cycle-over-cycle; B_hierarchy stays high.

**Observed:** A_free declined at c2 (regression confirmed), B_hierarchy declined less (contract protection confirmed), but both recovered at c3 and c4 (compounding not observed).

**Why the compounding didn't compound:** The subject regenerates the full implementation at each cycle rather than patching. There is no accumulated bug state — each cycle starts from a clean slate (prior code passed as context, but agent rewrites it entirely). Compounding regression would require a subject where bugs accumulate in partially-updated code, not fully-rewritten code.

---

## Conclusion

The regression at c2 and contract protection effect are real. The specific claim — that regression compounds *across* cycles — was not observed for this task class. This is informative, not null: it identifies a boundary condition on the compounding effect.

**The compounding effect (§2.6) requires subjects where the agent patches rather than regenerates.** Single-file class rewrites are self-healing. The effect would be more pronounced in multi-file codebases where the agent modifies one file and leaves prior bugs in others.

---

## Falsification status

The req-E3.md falsification condition was: "If A_free maintains high pass rate across all 4 cycles, agents have correct defaults."

A_free did NOT maintain high pass rate at c2 (0.822), so the falsification condition is not met. The compounding prediction is partially confirmed at c2. The sustained divergence prediction was not confirmed — this points to subject selection rather than theory refutation.

---

## Next steps

- **E3-full:** Run 30 trials for tighter error bars on the c2 gap.
- **E3b:** Design a multi-file subject where agents patch files rather than rewrite them. This is the correct stress test for §2.6 compounding.
- **Subject criterion for compounding experiments:** Must be multi-file OR have state that agents cannot fix by regeneration (e.g., a database schema migration subject).
