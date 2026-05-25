import pytest
from solution import TodoList


# --- cycle 1 ---

def test_add_and_list():
    t = TodoList()
    t.add("buy milk")
    assert t.list_items() == ["buy milk"]


def test_insertion_order():
    t = TodoList()
    t.add("b"); t.add("a")
    assert t.list_items() == ["b", "a"]


def test_empty():
    assert TodoList().list_items() == []


# --- cycle 2 ---

def test_complete_moves_to_done():
    t = TodoList()
    t.add("a"); t.add("b")
    t.complete("a")
    assert t.pending() == ["b"]
    assert t.done_items() == ["a"]


def test_list_items_includes_done():
    t = TodoList()
    t.add("a"); t.add("b")
    t.complete("a")
    assert t.list_items() == ["a", "b"]


def test_complete_not_found_raises():
    t = TodoList()
    with pytest.raises(ValueError):
        t.complete("z")
