"""Hidden judge suite for normalize_tags. Agent never sees this.

Superset of Arm D contracts. Same test cases, same expected outputs.
All decisions locked 2026-05-24 — see lab/docs/req-E2.md Section 6.
"""
from solution import normalize_tags


def test_hidden_lowercase_dedup():
    assert normalize_tags(["Python", "python"]) == ["python"]


def test_hidden_strip_and_dedup():
    assert normalize_tags(["  Go  ", "go"]) == ["go"]


def test_hidden_empty_string_dropped():
    assert normalize_tags(["", "rust"]) == ["rust"]


def test_hidden_whitespace_only_dropped():
    assert normalize_tags(["   "]) == []


def test_hidden_whitespace_only_in_mixed_list():
    assert normalize_tags(["   ", "rust"]) == ["rust"]


def test_hidden_none_dropped():
    assert normalize_tags([None, "go"]) == ["go"]


def test_hidden_order_preserving_dedup():
    assert normalize_tags(["b", "a", "b"]) == ["b", "a"]


def test_hidden_empty_input():
    assert normalize_tags([]) == []


def test_hidden_internal_whitespace_preserved():
    assert normalize_tags(["Hello World"]) == ["hello world"]
