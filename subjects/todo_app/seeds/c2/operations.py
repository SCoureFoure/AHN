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
