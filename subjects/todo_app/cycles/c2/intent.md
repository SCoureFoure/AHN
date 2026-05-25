# Intent — cycle 2: complete and filter

Add completion tracking to the todo app.

Changes needed:

- `models.py` — ensure `Task` has a `done: bool = False` field (add if not present)
- `operations.py` — add three methods to `TodoApp`:
  - `complete(title: str) -> None` — marks the matching task as done; raises `ValueError` if no task with that title exists
  - `pending_items() -> list[Task]` — returns tasks where `done == False`, in insertion order
  - `done_items() -> list[Task]` — returns tasks where `done == True`, in insertion order

`list_items()` must continue to return ALL tasks (both done and pending), in insertion order.
