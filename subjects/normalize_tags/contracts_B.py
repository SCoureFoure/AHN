"""Arm B contracts for normalize_tags — basic happy path only.

Two acceptance examples covering lowercase and dedup.
Edge cases (whitespace-only, None, empty input, sort order) are NOT covered.
"""
from solution import normalize_tags


def test_basic_lowercase():
    assert normalize_tags(["Python", "Go"]) == ["python", "go"]


def test_dedup():
    assert normalize_tags(["rust", "rust"]) == ["rust"]
