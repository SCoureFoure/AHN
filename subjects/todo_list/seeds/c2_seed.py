class TodoList:
    def __init__(self):
        self._items = []

    def add(self, item: str) -> None:
        self._items.append(item)

    def list_items(self) -> list[str]:
        return list(self._items)
