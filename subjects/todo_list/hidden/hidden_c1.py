"""Hidden judge suite — cycle 1 behaviors. Locked with todo_list subject."""
from solution import TodoList


def test_hidden_c1_add_single():
    t = TodoList()
    t.add("buy milk")
    assert t.list_items() == ["buy milk"]


def test_hidden_c1_insertion_order():
    t = TodoList()
    t.add("b")
    t.add("a")
    t.add("c")
    assert t.list_items() == ["b", "a", "c"]


def test_hidden_c1_empty():
    assert TodoList().list_items() == []


def test_hidden_c1_duplicates_allowed():
    t = TodoList()
    t.add("x")
    t.add("x")
    assert t.list_items() == ["x", "x"]
