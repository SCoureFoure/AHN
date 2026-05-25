# NOTE: These contracts cover only the basic cases.
# The function will be evaluated against additional edge cases not listed here.
# Implement defensively to handle inputs like empty strings, whitespace-only strings,
# None values, and duplicate detection after normalization.
from solution import normalize_tags


def test_basic_lowercase():
    assert normalize_tags(["Python", "Go"]) == ["python", "go"]


def test_dedup():
    assert normalize_tags(["rust", "rust"]) == ["rust"]
