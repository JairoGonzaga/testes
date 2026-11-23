import pytest

from alvo import intword


@pytest.mark.parametrize(
    "value, expected",
    [
        (-1000000, "-1.0 million"),
        (-1000, "-1.0 thousand"),
        (-2500000000, "-2.5 billion"),
        (-999999, "-1.0 million"),
        (-5, "-5"),
    ],
)
def test_negative_values_keep_minus_sign(value, expected):
    assert intword(value) == expected


def test_negative_value_with_custom_format_keeps_minus_sign():
    assert intword(-1500000, format="%.2f") == "-1.50 million"
