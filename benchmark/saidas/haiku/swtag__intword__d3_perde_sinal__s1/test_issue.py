import pytest

from alvo import intword


def test_negative_million_keeps_minus_sign():
    assert intword(-1000000) == "-1.0 million"


@pytest.mark.parametrize(
    "value, expected",
    [
        (-5, "-5"),
        (-999, "-999"),
        (-1000, "-1.0 thousand"),
        (-1500, "-1.5 thousand"),
        (-999999, "-1.0 million"),
        (-2500000000, "-2.5 billion"),
    ],
)
def test_negative_values_keep_minus_sign(value, expected):
    assert intword(value) == expected


def test_negative_value_with_custom_format_keeps_minus_sign():
    assert intword(-1000000, format="%.2f") == "-1.00 million"


def test_positive_value_still_has_no_sign():
    assert intword(1000000) == "1.0 million"
