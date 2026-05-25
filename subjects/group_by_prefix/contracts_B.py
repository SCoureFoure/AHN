"""Arm B contracts for group_by_prefix — basic happy path only.

Two acceptance examples covering basic grouping.
Edge cases (no-sep items, multi-sep items, empty prefix, duplicates, insertion order) are NOT covered.
"""
from solution import group_by_prefix


def test_basic():
    assert group_by_prefix(["a.x", "b.y"], ".") == {"a": ["x"], "b": ["y"]}


def test_multiple_values_same_prefix():
    assert group_by_prefix(["a.x", "a.y"], ".") == {"a": ["x", "y"]}
