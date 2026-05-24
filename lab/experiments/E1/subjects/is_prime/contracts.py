"""Arm B contracts for is_prime. Encodes the acceptance examples from req-E1.md.

These are given to the agent in Arm B. The agent must make them pass.
"""
from solution import is_prime


def test_is_prime_two():
    assert is_prime(2) is True


def test_is_prime_four():
    assert is_prime(4) is False


def test_is_prime_one():
    assert is_prime(1) is False


def test_is_prime_zero():
    assert is_prime(0) is False
