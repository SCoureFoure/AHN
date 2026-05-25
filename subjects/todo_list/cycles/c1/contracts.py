from solution import TodoList


def test_add_and_list():
    t = TodoList()
    t.add("buy milk")
    assert t.list_items() == ["buy milk"]


def test_insertion_order():
    t = TodoList()
    t.add("b")
    t.add("a")
    assert t.list_items() == ["b", "a"]


def test_empty():
    assert TodoList().list_items() == []
