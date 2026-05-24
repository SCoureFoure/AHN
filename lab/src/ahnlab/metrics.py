"""Divergence and aggregate metrics for experiments."""
from __future__ import annotations

from itertools import combinations
from statistics import mean


def hamming(a: list[int], b: list[int]) -> int:
    if len(a) != len(b):
        raise ValueError(f"vector length mismatch: {len(a)} vs {len(b)}")
    return sum(x != y for x, y in zip(a, b))


def mean_pairwise_hamming(vectors: list[list[int]]) -> float:
    if len(vectors) < 2:
        return 0.0
    return mean(hamming(a, b) for a, b in combinations(vectors, 2))


def pass_rate(vectors: list[list[int]]) -> float:
    if not vectors:
        return 0.0
    flat = [v for vec in vectors for v in vec]
    return sum(flat) / len(flat) if flat else 0.0
