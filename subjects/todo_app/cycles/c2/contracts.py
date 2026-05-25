"""Cycle 2 contracts — complete, pending_items, done_items (cumulative: includes c1)."""
import pytest
from models import Task
from operations import TodoApp


def test_add_returns_task():
    app = TodoApp()
    t = app.add("buy milk")
    assert isinstance(t, Task)
    assert t.title == "buy milk"


def test_list_items_insertion_order():
    app = TodoApp()
    app.add("a"); app.add("b"); app.add("c")
    assert [t.title for t in app.list_items()] == ["a", "b", "c"]


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
    titles = [t.title for t in app.pending_items()]
    assert titles == ["b"]


def test_done_items():
    app = TodoApp()
    app.add("a"); app.add("b")
    app.complete("a")
    titles = [t.title for t in app.done_items()]
    assert titles == ["a"]


def test_complete_missing_raises():
    app = TodoApp()
    with pytest.raises(ValueError):
        app.complete("ghost")
