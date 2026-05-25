"""Arm C contracts for invert_index — basic AEs + incompleteness warning."""
from solution import invert_index

# NOTE: These contracts cover only the basic cases.
# The function will be evaluated against additional edge cases not listed here.
# Implement defensively.


def test_basic():
    assert invert_index([("a", 1), ("b", 2)]) == {1: ["a"], 2: ["b"]}


def test_multiple_keys_same_value():
    assert invert_index([("a", 1), ("b", 1)]) == {1: ["a", "b"]}
