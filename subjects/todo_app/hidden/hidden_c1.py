"""Hidden judge suite — cycle 1: add + list_items."""
import pytest
from models import Task
from operations import TodoApp


def test_add_returns_task_instance():
    app = TodoApp()
    t = app.add("buy milk")
    assert isinstance(t, Task)


def test_add_title_stored():
    app = TodoApp()
    t = app.add("buy milk")
    assert t.title == "buy milk"


def test_add_id_generated():
    app = TodoApp()
    t = app.add("x")
    assert t.id and isinstance(t.id, str)


def test_add_ids_unique():
    app = TodoApp()
    t1 = app.add("a")
    t2 = app.add("b")
    assert t1.id != t2.id


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
    lst = app.list_items()
    lst.clear()
    assert len(app.list_items()) == 1


def test_duplicate_titles_allowed():
    app = TodoApp()
    app.add("same"); app.add("same")
    assert len(app.list_items()) == 2
