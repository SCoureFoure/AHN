# todo_app — multi-file training range subject

Two-file Python app used for E3b (multi-file compounding regression).

## Files

- `models.py` — `Task` dataclass: id, title, done, priority
- `operations.py` — `TodoApp` class: stateful operations on a list of Tasks

## Why two files

The regression surface is the interface between files. When agents add a feature to `operations.py`, they may fail to update `models.py` (or vice versa). Prior-cycle bugs in the untouched file persist across cycles — they cannot be healed by rewriting the other file.

## Cycles

| Cycle | Feature | Primary file | Regression risk |
|---|---|---|---|
| c1 | `add`, `list_items` | both | Baseline |
| c2 | `complete`, `pending_items`, `done_items` | operations.py | models.py Task.done field may be missing |
| c3 | `remove` | operations.py | Task lookup by title may corrupt state |
| c4 | Priority on `add`/`list_items` | models.py + operations.py | Cross-file: priority field added to Task but sort not updated in operations |
