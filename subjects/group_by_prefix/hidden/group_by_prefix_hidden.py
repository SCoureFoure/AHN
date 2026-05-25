"""Hidden judge suite for group_by_prefix. Agent never sees this.

Superset of Arm D contracts. Same test cases, same expected outputs.
All decisions locked 2026-05-24 — see lab/docs/req-E3.md Section 3.
"""
from solution import group_by_prefix


def test_hidden_basic():
    assert group_by_prefix(["a.x", "b.y"], ".") == {"a": ["x"], "b": ["y"]}


def test_hidden_multiple_values_same_prefix():
    assert group_by_prefix(["a.x", "a.y"], ".") == {"a": ["x", "y"]}


def test_hidden_item_with_no_separator():
    assert group_by_prefix(["a.x", "tag"], ".") == {"a": ["x"], "tag": [""]}


def test_hidden_single_item_no_separator():
    assert group_by_prefix(["tag"], ".") == {"tag": [""]}


def test_hidden_split_on_first_sep_only():
    assert group_by_prefix(["x.y.z"], ".") == {"x": ["y.z"]}


def test_hidden_empty_input():
    assert group_by_prefix([], ".") == {}


def test_hidden_duplicates_preserved():
    assert group_by_prefix(["a.x", "a.x"], ".") == {"a": ["x", "x"]}


def test_hidden_insertion_order_not_sorted():
    assert group_by_prefix(["b.2", "a.1"], ".") == {"b": ["2"], "a": ["1"]}


def test_hidden_empty_prefix():
    assert group_by_prefix([".x"], ".") == {"": ["x"]}
