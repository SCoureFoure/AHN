"""Arm D contracts for invert_index — all 9 acceptance examples (full coverage).

Locked 2026-05-24 — see lab/docs/req-E3.md Section 8.
"""
from solution import invert_index


def test_basic():
    assert invert_index([("a", 1), ("b", 2)]) == {1: ["a"], 2: ["b"]}


def test_multiple_keys_same_value():
    assert invert_index([("a", 1), ("b", 1)]) == {1: ["a", "b"]}


def test_exact_duplicate_pair_preserved():
    assert invert_index([("a", 1), ("a", 1)]) == {1: ["a", "a"]}


def test_empty_input():
    assert invert_index([]) == {}


def test_insertion_order_not_sorted():
    assert invert_index([("b", 2), ("a", 1)]) == {2: ["b"], 1: ["a"]}


def test_non_contiguous_grouping():
    assert invert_index([("a", 1), ("b", 2), ("c", 1)]) == {1: ["a", "c"], 2: ["b"]}


def test_key_reappears_with_same_value():
    assert invert_index([("a", 1), ("b", 1), ("a", 1)]) == {1: ["a", "b", "a"]}


def test_single_pair_string_value():
    assert invert_index([("a", "x")]) == {"x": ["a"]}


def test_same_key_multiple_values_then_dup():
    assert invert_index([("a", 1), ("a", 2), ("a", 1)]) == {1: ["a", "a"], 2: ["a"]}
