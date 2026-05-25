"""Hidden judge suite — cycle 4: all prior regression + priority."""
import pytest
from models import Task
from operations import TodoApp


# --- c1 regression ---

def test_add_returns_task_instance():
    app = TodoApp()
    assert isinstance(app.add("x"), Task)


def test_list_items_empty():
    app = TodoApp()
    assert app.list_items() == []


# --- c2 regression ---

def test_task_done_default_false():
    app = TodoApp()
    assert app.add("x").done is False


def test_complete_sets_done():
    app = TodoApp()
    app.add("x")
    app.complete("x")
    assert app.list_items()[0].done is True


def test_pending_excludes_done():
    app = TodoApp()
    app.add("a"); app.add("b")
    app.complete("a")
    assert [t.title for t in app.pending_items()] == ["b"]


def test_done_items():
    app = TodoApp()
    app.add("a"); app.add("b")
    app.complete("a")
    assert [t.title for t in app.done_items()] == ["a"]


def test_complete_missing_raises():
    app = TodoApp()
    with pytest.raises(ValueError):
        app.complete("ghost")


# --- c3 regression ---

def test_remove_task():
    app = TodoApp()
    app.add("a"); app.add("b"); app.add("c")
    app.remove("b")
    assert [t.title for t in app.list_items()] == ["a", "c"]


def test_remove_missing_raises():
    app = TodoApp()
    with pytest.raises(ValueError):
        app.remove("ghost")


# --- c4 ---

def test_task_priority_field_default_zero():
    app = TodoApp()
    t = app.add("x")
    assert t.priority == 0


def test_add_with_priority():
    app = TodoApp()
    t = app.add("x", priority=3)
    assert t.priority == 3


def test_list_items_sorted_by_priority_desc():
    app = TodoApp()
    app.add("low", priority=0)
    app.add("high", priority=2)
    app.add("mid", priority=1)
    assert [t.title for t in app.list_items()] == ["high", "mid", "low"]


def test_equal_priority_insertion_order():
    app = TodoApp()
    app.add("first", priority=1)
    app.add("second", priority=1)
    app.add("third", priority=1)
    assert [t.title for t in app.list_items()] == ["first", "second", "third"]


def test_add_no_priority_defaults_zero():
    app = TodoApp()
    t = app.add("plain")
    assert t.priority == 0


def test_pending_sorted_by_priority():
    app = TodoApp()
    app.add("low", priority=0)
    app.add("high", priority=2)
    app.complete("high")
    app.add("mid", priority=1)
    assert [t.title for t in app.pending_items()] == ["mid", "low"]


def test_done_sorted_by_priority():
    app = TodoApp()
    app.add("lo", priority=0)
    app.add("hi", priority=2)
    app.complete("lo")
    app.complete("hi")
    assert [t.title for t in app.done_items()] == ["hi", "lo"]


def test_remove_then_priority_sort():
    app = TodoApp()
    app.add("a", priority=1)
    app.add("b", priority=3)
    app.add("c", priority=2)
    app.remove("b")
    assert [t.title for t in app.list_items()] == ["c", "a"]
