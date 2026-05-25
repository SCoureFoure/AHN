"""Hidden judge suite for is_prime. Agent never sees this.

Superset of the Arm B contracts. Adds edge cases the requirement is silent on,
to surface interpretation drift.
"""
import pytest
from solution import is_prime


def test_hidden_is_prime_two():
    assert is_prime(2) is True


def test_hidden_is_prime_three():
    assert is_prime(3) is True


def test_hidden_is_prime_four():
    assert is_prime(4) is False


def test_hidden_is_prime_one():
    assert is_prime(1) is False


def test_hidden_is_prime_zero():
    assert is_prime(0) is False


def test_hidden_is_prime_negative():
    assert is_prime(-7) is False


def test_hidden_is_prime_large_prime():
    assert is_prime(7919) is True


def test_hidden_is_prime_large_composite():
    assert is_prime(7920) is False


def test_hidden_is_prime_typeerror_on_float():
    with pytest.raises((TypeError, ValueError)):
        is_prime(3.0)
