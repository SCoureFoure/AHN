# E3 Requirements — Compounding Regression

**Experiment ID:** E3  
**Status:** Ready  
**Subject:** `todo_list` (see `subjects/todo_list/meta.md`)  
**Bias probed:** Without contract accumulation, agent regressions compound across feature cycles.

---

## Research Question

Does regression rate diverge between a hierarchy-first arm (cumulative contracts at each cycle) and a free-edit arm (no contracts) as feature cycles accumulate?

Prediction: A_free pass rate declines each cycle as prior behaviors are silently broken. B_hierarchy pass rate stays high because the cumulative contract suite forces the agent to satisfy all prior behaviors simultaneously.

If both arms show equivalent pass rates across all cycles, the compounding effect (§2.6) is not present for this task class and this model.

---

## Arms

| Arm | Contracts | Prediction |
|---|---|---|
| A_free | None at any cycle | Pass rate declines cycle-over-cycle |
| B_hierarchy | Cumulative contracts at each cycle | Pass rate stays high |

---

## Cycles

| Cycle | Feature | Key regression risk |
|---|---|---|
| c1 | `add`, `list_items` | Baseline |
| c2 | `complete`, `pending`, `done_items` | `list_items` filtered to pending only |
| c3 | `remove` | Order corruption, done/pending state broken |
| c4 | Priority on `add`/`list_items`/`pending` | Insertion-order tiebreak, backward compat |

---

## Run Parameters

| Parameter | Value |
|---|---|
| Model | `claude-haiku-4-5-20251001` |
| Temperature | 0.7 |
| Trials per arm | 10 (pilot) → 30 (full) |
| Cycles | 4 |
| Total API calls (pilot) | 80 |
| Estimated cost (pilot) | ~$1.60 |

---

## Metrics

- Hidden pass rate per (arm, cycle): fraction of cumulative hidden tests passing at that cycle
- Regression signal: declining pass rate in A_free arm on prior-cycle tests as N increases
- Cost per chain: sum across 4 cycles

---

## Falsification

If A_free maintains high pass rate across all 4 cycles: agents have correct defaults for this refactoring task class, and the compounding effect is not measurable here. Subject selection would need revision (more complex subject with stronger regression surface).
