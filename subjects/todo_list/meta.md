# todo_list

**Bias probed:** Compounding regression without contract accumulation (E3).

Each feature cycle requires modifying existing methods, not just adding new ones. An agent that
ignores prior behavior will silently break it. The hierarchy arm accumulates contracts each cycle;
the free-edit arm has none. The hidden suite at cycle N tests all behaviors from cycles 1..N.

## Cycles

| Cycle | Feature added | Regression surface |
|---|---|---|
| c1 | `add`, `list_items` | Baseline — insertion order, duplicates |
| c2 | `complete`, `pending`, `done_items` | Must NOT filter `list_items` to pending only |
| c3 | `remove` | Must update pending/done state; order preserved |
| c4 | Priority on `add`/`list_items`/`pending` | Insertion order tiebreak; backward compat; done items still in list |

## Files

- `cycles/cN/intent.md` — feature request the agent sees at cycle N
- `cycles/cN/contracts.py` — cumulative contracts shown to hierarchy arm at cycle N
- `seeds/cN_seed.py` — correct implementation through cycle N-1 (agent starting point)
- `hidden/hidden_cN.py` — cumulative hidden suite through cycle N (never shown to agent)
