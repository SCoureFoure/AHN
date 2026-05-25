"""Arm B contracts for invert_index — basic happy path only.

Two acceptance examples covering basic inversion.
Edge cases (duplicate pairs, repeated keys, insertion order) are NOT covered.
"""
from solution import invert_index


def test_basic():
    assert invert_index([("a", 1), ("b", 2)]) == {1: ["a"], 2: ["b"]}


def test_multiple_keys_same_value():
    assert invert_index([("a", 1), ("b", 1)]) == {1: ["a", "b"]}
