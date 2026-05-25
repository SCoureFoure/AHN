# Intent — cycle 3: remove

Add task removal to the todo app.

Changes needed:

- `operations.py` — add one method to `TodoApp`:
  - `remove(title: str) -> None` — removes the first task with that title from the list; raises `ValueError` if no task with that title exists

All prior methods (`add`, `list_items`, `complete`, `pending_items`, `done_items`) must continue working correctly. Removing a task must preserve the insertion order of the remaining tasks. The `done` state of remaining tasks must be unaffected.
