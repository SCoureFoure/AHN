"""Hidden judge suite — cycle 2: c1 regression + complete/pending/done."""
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


def test_list_items_returns_copy():
    app = TodoApp()
    app.add("a")
    app.list_items().clear()
    assert len(app.list_items()) == 1


# --- c2 ---

def test_task_done_field_default_false():
    app = TodoApp()
    t = app.add("x")
    assert t.done is False


def test_complete_sets_done_true():
    app = TodoApp()
    app.add("wash car")
    app.complete("wash car")
    assert app.list_items()[0].done is True


def test_list_items_includes_done_tasks():
    app = TodoApp()
    app.add("a"); app.add("b")
    app.complete("a")
    assert len(app.list_items()) == 2


def test_pending_items_excludes_done():
    app = TodoApp()
    app.add("a"); app.add("b")
    app.complete("a")
    assert [t.title for t in app.pending_items()] == ["b"]


def test_pending_items_empty_when_all_done():
    app = TodoApp()
    app.add("a")
    app.complete("a")
    assert app.pending_items() == []


def test_done_items_correct():
    app = TodoApp()
    app.add("a"); app.add("b")
    app.complete("a")
    assert [t.title for t in app.done_items()] == ["a"]


def test_done_items_empty_initially():
    app = TodoApp()
    app.add("a")
    assert app.done_items() == []


def test_complete_missing_raises_value_error():
    app = TodoApp()
    with pytest.raises(ValueError):
        app.complete("ghost")


def test_complete_only_first_matching():
    app = TodoApp()
    app.add("dup"); app.add("dup")
    app.complete("dup")
    done = app.done_items()
    pending = app.pending_items()
    assert len(done) == 1 and len(pending) == 1
