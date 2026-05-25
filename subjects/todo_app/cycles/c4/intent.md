# Intent — cycle 4: priority

Add a priority field to tasks and sort list output accordingly.

Changes needed:

- `models.py` — add `priority: int = 0` to `Task` (higher number = higher priority)
- `operations.py` — update `add(title: str, priority: int = 0) -> Task` to accept and store priority; update `list_items()` to return tasks sorted by priority descending, with equal-priority tasks in insertion order (stable sort)

`pending_items()` and `done_items()` must also return results sorted by priority descending with equal-priority insertion order preserved.

Backward compatibility: `add(title)` with no priority must still work (defaults to 0).
