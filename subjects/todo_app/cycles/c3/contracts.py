"""Cycle 3 contracts — remove (cumulative: includes c1+c2)."""
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


def test_remove_pending():
    app = TodoApp()
    app.add("a"); app.add("b"); app.add("c")
    app.remove("b")
    assert [t.title for t in app.list_items()] == ["a", "c"]


def test_remove_done():
    app = TodoApp()
    app.add("a"); app.add("b")
    app.complete("a")
    app.remove("a")
    assert [t.title for t in app.list_items()] == ["b"]
    assert app.done_items() == []


def test_remove_missing_raises():
    app = TodoApp()
    with pytest.raises(ValueError):
        app.remove("ghost")
