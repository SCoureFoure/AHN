"""Hidden judge suite for invert_index. Agent never sees this.

Superset of Arm D contracts. Same test cases, same expected outputs.
All decisions locked 2026-05-24 — see lab/docs/req-E3.md Section 8.
"""
from solution import invert_index


def test_hidden_basic():
    assert invert_index([("a", 1), ("b", 2)]) == {1: ["a"], 2: ["b"]}


def test_hidden_multiple_keys_same_value():
    assert invert_index([("a", 1), ("b", 1)]) == {1: ["a", "b"]}


def test_hidden_exact_duplicate_pair_preserved():
    assert invert_index([("a", 1), ("a", 1)]) == {1: ["a", "a"]}


def test_hidden_empty_input():
    assert invert_index([]) == {}


def test_hidden_insertion_order_not_sorted():
    assert invert_index([("b", 2), ("a", 1)]) == {2: ["b"], 1: ["a"]}


def test_hidden_non_contiguous_grouping():
    assert invert_index([("a", 1), ("b", 2), ("c", 1)]) == {1: ["a", "c"], 2: ["b"]}


def test_hidden_key_reappears_with_same_value():
    assert invert_index([("a", 1), ("b", 1), ("a", 1)]) == {1: ["a", "b", "a"]}


def test_hidden_single_pair_string_value():
    assert invert_index([("a", "x")]) == {"x": ["a"]}


def test_hidden_same_key_multiple_values_then_dup():
    assert invert_index([("a", 1), ("a", 2), ("a", 1)]) == {1: ["a", "a"], 2: ["a"]}
