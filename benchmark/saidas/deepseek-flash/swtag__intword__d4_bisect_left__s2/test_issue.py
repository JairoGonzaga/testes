"""Reproduction tests for: intword(10**100) should return '1.0 googol'."""

import pytest

from alvo import intword


def test_googol_exact():
    assert intword(10**100) == "1.0 googol"


def test_googol_exact_negative():
    assert intword(-(10**100)) == "-1.0 googol"


def test_googol_not_previous_suffix():
    result = intword(10**100)
    assert "decillion" not in result
    assert result.endswith("googol")


@pytest.mark.parametrize("value", [10**100, -(10**100)])
def test_googol_uses_right_unit(value):
    """The value must be expressed in googols, not in the largest lower unit."""
    result = intword(value, "%d")
    expected_sign = "-" if value < 0 else ""
    assert result == f"{expected_sign}1 googol"
