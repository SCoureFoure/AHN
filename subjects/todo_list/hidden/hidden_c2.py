"""Hidden judge suite — cumulative through cycle 2. Locked with todo_list subject."""
import pytest
from solution import TodoList


# --- cycle 1 regression ---

def test_hidden_c1_add_single():
    t = TodoList()
    t.add("buy milk")
    assert t.list_items() == ["buy milk"]


def test_hidden_c1_insertion_order():
    t = TodoList()
    t.add("b"); t.add("a"); t.add("c")
    assert t.list_items() == ["b", "a", "c"]


def test_hidden_c1_empty():
    assert TodoList().list_items() == []


def test_hidden_c1_duplicates_allowed():
    t = TodoList()
    t.add("x"); t.add("x")
    assert t.list_items() == ["x", "x"]


# --- cycle 2 ---

def test_hidden_c2_all_start_pending():
    t = TodoList()
    t.add("a"); t.add("b"); t.add("c")
    assert t.pending() == ["a", "b", "c"]
    assert t.done_items() == []


def test_hidden_c2_complete_moves_item():
    t = TodoList()
    t.add("a"); t.add("b"); t.add("c")
    t.complete("b")
    assert t.pending() == ["a", "c"]
    assert t.done_items() == ["b"]


def test_hidden_c2_list_items_includes_done():
    t = TodoList()
    t.add("a"); t.add("b")
    t.complete("a")
    assert t.list_items() == ["a", "b"]


def test_hidden_c2_complete_not_found_raises():
    t = TodoList()
    t.add("a")
    with pytest.raises(ValueError):
        t.complete("z")


def test_hidden_c2_done_preserves_insertion_order():
    t = TodoList()
    t.add("a"); t.add("b"); t.add("c")
    t.complete("a"); t.complete("c")
    assert t.done_items() == ["a", "c"]
