"""Reproduction tests for the `intword` suffix-promotion bug.

Issue: when rounding pushes the mantissa up to 1000, the unit suffix is not
promoted, e.g. ``intword(999999)`` returns ``'1000.0 thousand'`` instead of
``'1.0 million'``.
"""

import pytest

from alvo import intword


@pytest.mark.parametrize(
    "value, expected",
    [
        # Exact example from the issue report.
        (999999, "1.0 million"),
        # Same bug one and two orders of magnitude further up.
        (999_999_999, "1.0 billion"),
        (999_999_999_999, "1.0 trillion"),
        # Largest value that still rounds up (999.95 -> 1000.0).
        (999_950, "1.0 million"),
        # A value whose rounding pushes it from nonillion to decillion.
        (10**33 - 1, "1.0 decillion"),
    ],
)
def test_rounding_up_promotes_the_suffix(value, expected):
    assert intword(value) == expected


@pytest.mark.parametrize(
    "value, expected",
    [
        (-999999, "-1.0 million"),
        (-999_999_999, "-1.0 billion"),
    ],
)
def test_rounding_up_promotes_the_suffix_for_negative_values(value, expected):
    assert intword(value) == expected


def test_rounding_up_promotion_does_not_emit_a_thousand_mantissa():
    for value in (999_999, 999_999_999, 999_999_999_999, 10**33 - 1):
        result = intword(value)
        mantissa = result.split()[0]
        assert not mantissa.startswith(("1000", "-1000")), (
            f"intword({value}) returned {result!r}, which keeps a 1000 mantissa"
        )
        assert mantissa.lstrip("-") == "1.0"


@pytest.mark.parametrize(
    "value, expected",
    [
        # Values that round up but not all the way to the next power.
        (999, "999"),
        (1499, "1.5 thousand"),
        (999_949, "999.9 thousand"),
        (1_999_999, "2.0 million"),
        # Boundary values that must be unaffected.
        (1000, "1.0 thousand"),
        (1_000_000, "1.0 million"),
    ],
)
def test_unaffected_values_still_format_correctly(value, expected):
    assert intword(value) == expected
