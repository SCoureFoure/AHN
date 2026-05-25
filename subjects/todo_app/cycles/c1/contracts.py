"""Cycle 1 contracts — add and list_items."""
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
    app.add("a")
    app.add("b")
    app.add("c")
    titles = [t.title for t in app.list_items()]
    assert titles == ["a", "b", "c"]


def test_list_items_empty():
    app = TodoApp()
    assert app.list_items() == []
