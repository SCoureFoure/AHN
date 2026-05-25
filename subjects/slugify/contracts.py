"""Arm B contracts for slugify."""
from solution import slugify


def test_slugify_hello_world():
    assert slugify("Hello World") == "hello-world"


def test_slugify_trim():
    assert slugify("  Trim Me  ") == "trim-me"


def test_slugify_collapse_dashes():
    assert slugify("multi---dash") == "multi-dash"
