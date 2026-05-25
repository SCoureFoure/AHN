"""Hidden judge suite for slugify."""
from solution import slugify


def test_hidden_slugify_hello_world():
    assert slugify("Hello World") == "hello-world"


def test_hidden_slugify_trim():
    assert slugify("  Trim Me  ") == "trim-me"


def test_hidden_slugify_collapse_dashes():
    assert slugify("multi---dash") == "multi-dash"


def test_hidden_slugify_empty():
    assert slugify("") == ""


def test_hidden_slugify_only_punctuation():
    assert slugify("!!!") == ""


def test_hidden_slugify_unicode_strip():
    # Reasonable interpretations: strip diacritics OR drop unknown chars.
    # Accept either "cafe" or "" but not raise.
    result = slugify("Café")
    assert result in {"cafe", "caf", ""}


def test_hidden_slugify_leading_trailing_punctuation():
    assert slugify("--hello--") == "hello"


def test_hidden_slugify_underscores():
    # Spec silent; accept either "snake-case" or "snake_case".
    result = slugify("snake_case")
    assert result in {"snake-case", "snake_case"}


def test_hidden_slugify_numeric():
    assert slugify("Order 66") == "order-66"
