class TodoList:
    def __init__(self):
        self._items = []  # list of [item: str, done: bool]

    def add(self, item: str) -> None:
        self._items.append([item, False])

    def list_items(self) -> list[str]:
        return [entry[0] for entry in self._items]

    def complete(self, item: str) -> None:
        for entry in self._items:
            if entry[0] == item:
                entry[1] = True
                return
        raise ValueError(f"{item!r} not found")

    def pending(self) -> list[str]:
        return [entry[0] for entry in self._items if not entry[1]]

    def done_items(self) -> list[str]:
        return [entry[0] for entry in self._items if entry[1]]

    def remove(self, item: str) -> None:
        for i, entry in enumerate(self._items):
            if entry[0] == item:
                del self._items[i]
                return
        raise ValueError(f"{item!r} not found")
