"""TodoApp operations."""
from models import Task


class TodoApp:
    def __init__(self) -> None:
        self._tasks: list[Task] = []

    def add(self, title: str) -> Task:
        task = Task(title=title)
        self._tasks.append(task)
        return task

    def list_items(self) -> list[Task]:
        return list(self._tasks)

    def complete(self, title: str) -> None:
        for task in self._tasks:
            if task.title == title:
                task.done = True
                return
        raise ValueError(f"Task not found: {title!r}")

    def pending_items(self) -> list[Task]:
        return [t for t in self._tasks if not t.done]

    def done_items(self) -> list[Task]:
        return [t for t in self._tasks if t.done]

    def remove(self, title: str) -> None:
        for i, task in enumerate(self._tasks):
            if task.title == title:
                del self._tasks[i]
                return
        raise ValueError(f"Task not found: {title!r}")
