"""Smoke tests for metrics — no API required."""
from ahnlab.metrics import hamming, mean_pairwise_hamming, pass_rate


def test_hamming_zero():
    assert hamming([1, 0, 1], [1, 0, 1]) == 0


def test_hamming_count():
    assert hamming([1, 0, 1, 0], [0, 0, 1, 1]) == 2


def test_mean_pairwise_zero_when_identical():
    vectors = [[1, 0, 1]] * 5
    assert mean_pairwise_hamming(vectors) == 0.0


def test_mean_pairwise_nonzero_when_diverse():
    vectors = [[1, 0, 1], [0, 0, 1], [1, 1, 1]]
    assert mean_pairwise_hamming(vectors) > 0.0


def test_pass_rate_basic():
    assert pass_rate([[1, 1, 0], [1, 0, 0]]) == 3 / 6


def test_pass_rate_empty():
    assert pass_rate([]) == 0.0
