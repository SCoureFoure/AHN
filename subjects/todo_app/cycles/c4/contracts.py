"""Cycle 4 contracts — priority (cumulative: includes c1+c2+c3)."""
import pytest
from models import Task
from operations import TodoApp


def test_add_returns_task():
    app = TodoApp()
    t = app.add("buy milk")
    assert isinstance(t, Task)
    assert t.title == "buy milk"


def test_list_items_empty():
    app = TodoApp()
    assert app.list_items() == []


def test_complete_marks_done():
    app = TodoApp()
    app.add("wash car")
    app.complete("wash car")
    assert app.list_items()[0].done is True


def test_list_items_includes_done():
    app = TodoApp()
    app.add("a"); app.add("b")
    app.complete("a")
    assert len(app.list_items()) == 2


def test_pending_items_excludes_done():
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


def test_remove_missing_raises():
    app = TodoApp()
    with pytest.raises(ValueError):
        app.remove("ghost")


def test_priority_sort():
    app = TodoApp()
    app.add("low", priority=0)
    app.add("high", priority=2)
    app.add("mid", priority=1)
    titles = [t.title for t in app.list_items()]
    assert titles == ["high", "mid", "low"]


def test_equal_priority_insertion_order():
    app = TodoApp()
    app.add("first", priority=1)
    app.add("second", priority=1)
    titles = [t.title for t in app.list_items()]
    assert titles == ["first", "second"]


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
    titles = [t.title for t in app.pending_items()]
    assert titles == ["mid", "low"]
