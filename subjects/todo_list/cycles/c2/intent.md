# TodoList — Cycle 2: Done/pending tracking

Extend the existing `TodoList` class with done/pending tracking.

Add these methods:

- `complete(item: str) -> None` — mark the first matching item as done. Raises `ValueError` if item not in the list.
- `pending() -> list[str]` — return items not yet done, in insertion order
- `done_items() -> list[str]` — return completed items in insertion order

`list_items()` must continue to return ALL items (pending and done) in insertion order.
