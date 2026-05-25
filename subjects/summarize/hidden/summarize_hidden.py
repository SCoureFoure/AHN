"""Hidden judge suite for summarize."""
import pytest
from solution import summarize


def test_hidden_summarize_empty():
    result = summarize([])
    assert result["count"] == 0
    assert result["total"] == 0.0


def test_hidden_summarize_two_items():
    result = summarize([
        {"price": 1.0, "qty": 2},
        {"price": 3.0, "qty": 1},
    ])
    assert result["count"] == 2
    assert result["total"] == 5.0


def test_hidden_summarize_missing_qty():
    result = summarize([{"price": 4.0}])
    assert result["count"] == 1
    assert result["total"] == 4.0


def test_hidden_summarize_missing_price_raises():
    with pytest.raises((KeyError, ValueError, TypeError)):
        summarize([{"qty": 2}])


def test_hidden_summarize_negative_price_passthrough():
    result = summarize([{"price": -2.0, "qty": 3}])
    assert result["count"] == 1
    assert result["total"] == -6.0


def test_hidden_summarize_large_list():
    items = [{"price": 1.0, "qty": 1}] * 1000
    result = summarize(items)
    assert result["count"] == 1000
    assert result["total"] == 1000.0


def test_hidden_summarize_does_not_invent_currency_key():
    # Requirement is silent on currency. Output must not invent one.
    result = summarize([{"price": 1.0, "qty": 1}])
    assert "currency" not in result
