"""Arm D contracts for normalize_tags — full coverage of all edge cases."""
from solution import normalize_tags


def test_basic_lowercase():
    assert normalize_tags(["Python", "Go"]) == ["python", "go"]


def test_dedup():
    assert normalize_tags(["rust", "rust"]) == ["rust"]


def test_strip_and_dedup():
    assert normalize_tags(["  Go  ", "go"]) == ["go"]


def test_empty_string_dropped():
    assert normalize_tags(["", "rust"]) == ["rust"]


def test_whitespace_only_dropped():
    assert normalize_tags(["   "]) == []


def test_whitespace_only_in_mixed_list():
    assert normalize_tags(["   ", "rust"]) == ["rust"]


def test_none_dropped():
    assert normalize_tags([None, "go"]) == ["go"]


def test_order_preserving_dedup():
    assert normalize_tags(["b", "a", "b"]) == ["b", "a"]


def test_empty_input():
    assert normalize_tags([]) == []


def test_internal_whitespace_preserved():
    assert normalize_tags(["Hello World"]) == ["hello world"]
