"""Hidden judge suite — cycle 3: c1+c2 regression + remove."""
import pytest
from models import Task
from operations import TodoApp


# --- c1 regression ---

def test_add_returns_task_instance():
    app = TodoApp()
    assert isinstance(app.add("x"), Task)


def test_list_items_insertion_order():
    app = TodoApp()
    app.add("a"); app.add("b"); app.add("c")
    assert [t.title for t in app.list_items()] == ["a", "b", "c"]


def test_list_items_empty():
    app = TodoApp()
    assert app.list_items() == []


# --- c2 regression ---

def test_task_done_field_default_false():
    app = TodoApp()
    assert app.add("x").done is False


def test_complete_sets_done_true():
    app = TodoApp()
    app.add("x")
    app.complete("x")
    assert app.list_items()[0].done is True


def test_list_items_includes_done():
    app = TodoApp()
    app.add("a"); app.add("b")
    app.complete("a")
    assert len(app.list_items()) == 2


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


# --- c3 ---

def test_remove_pending_task():
    app = TodoApp()
    app.add("a"); app.add("b"); app.add("c")
    app.remove("b")
    assert [t.title for t in app.list_items()] == ["a", "c"]


def test_remove_done_task():
    app = TodoApp()
    app.add("a"); app.add("b")
    app.complete("a")
    app.remove("a")
    assert [t.title for t in app.list_items()] == ["b"]
    assert app.done_items() == []


def test_remove_preserves_done_state_of_others():
    app = TodoApp()
    app.add("a"); app.add("b"); app.add("c")
    app.complete("b")
    app.remove("a")
    assert app.list_items()[0].title == "b"
    assert app.list_items()[0].done is True


def test_remove_missing_raises():
    app = TodoApp()
    with pytest.raises(ValueError):
        app.remove("ghost")


def test_remove_preserves_insertion_order():
    app = TodoApp()
    for ch in "abcde":
        app.add(ch)
    app.remove("c")
    assert [t.title for t in app.list_items()] == ["a", "b", "d", "e"]
