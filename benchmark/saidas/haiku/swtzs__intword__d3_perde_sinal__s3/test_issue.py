import pytest

from alvo import intword


def test_negative_million_keeps_minus_sign():
    # Issue: intword(-1000000) returns '1.0 million' instead of '-1.0 million'.
    assert intword(-1000000) == "-1.0 million"


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        (-1000, "-1.0 thousand"),
        (-1500, "-1.5 thousand"),
        (-2500000000, "-2.5 billion"),
        (-999, "-999"),
    ],
)
def test_negative_values_keep_minus_sign(value, expected):
    assert intword(value) == expected


def test_positive_million_unchanged():
    assert intword(1000000) == "1.0 million"
