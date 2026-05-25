# TodoList — Cycle 4: Priority

Extend the existing `TodoList` class with priority support.

Changes required:

- `add(item: str, priority: int = 0) -> None` — accepts an optional priority (default 0). Higher number = higher priority. Calls without `priority` must still work.
- `list_items() -> list[str]` — now returns items sorted by priority descending. Items with equal priority preserve insertion order.
- `pending() -> list[str]` — same sort order as `list_items` (priority desc, insertion order for ties).

`done_items()` and `remove()` are unchanged. `list_items()` still returns all items (pending and done).
