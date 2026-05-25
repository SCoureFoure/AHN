# Intent — cycle 1: add and list

Implement a two-file todo application:

- `models.py` — defines a `Task` dataclass with fields: `title: str`, `id: str` (auto-generated unique id), `done: bool = False`
- `operations.py` — defines a `TodoApp` class with:
  - `add(title: str) -> Task` — creates a Task, appends to internal list, returns it
  - `list_items() -> list[Task]` — returns all tasks in insertion order

`operations.py` imports `Task` from `models.py` using an absolute import (`from models import Task`).
