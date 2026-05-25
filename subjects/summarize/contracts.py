"""Arm B contracts for summarize."""
from solution import summarize


def test_summarize_empty():
    result = summarize([])
    assert result["count"] == 0
    assert result["total"] == 0.0


def test_summarize_two_items():
    result = summarize([
        {"price": 1.0, "qty": 2},
        {"price": 3.0, "qty": 1},
    ])
    assert result["count"] == 2
    assert result["total"] == 5.0


def test_summarize_missing_qty_treated_as_one():
    result = summarize([{"price": 4.0}])
    assert result["count"] == 1
    assert result["total"] == 4.0
