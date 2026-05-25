"""Arm C contracts for group_by_prefix — basic AEs + incompleteness warning."""
from solution import group_by_prefix

# NOTE: These contracts cover only the basic cases.
# The function will be evaluated against additional edge cases not listed here.
# Implement defensively.


def test_basic():
    assert group_by_prefix(["a.x", "b.y"], ".") == {"a": ["x"], "b": ["y"]}


def test_multiple_values_same_prefix():
    assert group_by_prefix(["a.x", "a.y"], ".") == {"a": ["x", "y"]}
