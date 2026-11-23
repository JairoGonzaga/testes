"""Tests reproducing the issue: rounding must promote to the next suffix.

Bug: ``intword(999999)`` returns ``'1000.0 thousand'`` instead of
``'1.0 million'``.  When the mantissa is rounded up to the next power of a
thousand, the unit must be promoted as well (and the mantissa reset to 1.0).
"""

import pytest

from alvo import intword

# Exponents where the *next* unit is exactly 1000x larger, so a mantissa that
# rounds up to 1000.0 must be expressed as 1.0 of the next unit.
HUMAN_SCALE_EXPONENTS = [6, 9, 12, 15, 18, 21]

_UNIT_ORDER = [
    "thousand",
    "million",
    "billion",
    "trillion",
    "quadrillion",
    "quintillion",
    "sextillion",
    "septillion",
    "octillion",
    "nonillion",
    "decillion",
    "googol",
]


def test_issue_example():
    """The exact case from the issue report."""
    assert intword(999999) == "1.0 million"


def test_issue_example_negative():
    assert intword(-999999) == "-1.0 million"


@pytest.mark.parametrize(
    "value,expected",
    [
        (999999, "1.0 million"),
        (999999999, "1.0 billion"),
        (999999999999, "1.0 trillion"),
        (999999999999999, "1.0 quadrillion"),
        (999999999999999999, "1.0 quintillion"),
        (999999999999999999999, "1.0 sextillion"),
    ],
)
def test_rounding_up_promotes_suffix(value, expected):
    assert intword(value) == expected


@pytest.mark.parametrize(
    "value,expected",
    [
        (999950, "1.0 million"),
        (999960, "1.0 million"),
        (999999, "1.0 million"),
        (-999960, "-1.0 million"),
        (-999999, "-1.0 million"),
    ],
)
def test_rounding_to_one_thousand_promotes(value, expected):
    assert intword(value) == expected


@pytest.mark.parametrize(
    "value,expected",
    [
        (999900, "999.9 thousand"),
        (999899, "999.9 thousand"),
        (1234, "1.2 thousand"),
        (1000000, "1.0 million"),
        (1999999, "2.0 million"),
    ],
)
def test_no_promotion_when_not_rounding_up(value, expected):
    """Values that do not round up to 1000.0 must keep their suffix."""
    assert intword(value) == expected


@pytest.mark.parametrize("exponent", HUMAN_SCALE_EXPONENTS)
def test_mantissa_never_reaches_one_thousand(exponent):
    """A formatted mantissa of 1000.0 must never be shown with a suffix.

    If the mantissa rounds up to 1000.0, the value must be expressed with the
    next unit and a mantissa of 1.0 instead.
    """
    value = 10**exponent - 1
    result = intword(value)
    mantissa, _, unit = result.partition(" ")
    assert float(mantissa) < 1000.0, f"intword({value}) == {result!r}"
    expected_unit = _UNIT_ORDER[exponent // 3 - 1]
    assert unit == expected_unit, f"intword({value}) == {result!r}"
    assert float(mantissa) == 1.0, f"intword({value}) == {result!r}"


def test_custom_format_also_promotes():
    assert intword(999999, "%.0f") == "1 million"
    assert intword(999999, "%.2f") == "1.00 million"


def test_small_values_unaffected():
    assert intword(0) == "0"
    assert intword(999) == "999"
    assert intword(-999) == "-999"
    assert intword(1000) == "1.0 thousand"
    assert intword(-1000) == "-1.0 thousand"
