import pytest

from alvo import intword


def test_negative_million_keeps_sign():
    assert intword(-1000000) == "-1.0 million"


def test_negative_thousand_keeps_sign():
    assert intword(-1500) == "-1.5 thousand"


def test_negative_below_thousand_keeps_sign():
    assert intword(-500) == "-500"


@pytest.mark.parametrize(
    "value",
    [-1, -999, -1000, -1500000, -2.5e9, -3e12, -7.25e18, -1e30],
)
def test_negative_is_minus_sign_plus_positive(value):
    assert intword(value) == "-" + intword(-value)
