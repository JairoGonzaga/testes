"""Tests reproducing the issue: intword(999999) returns '1000.0 thousand'.

When rounding pushes a value up to the next power of ten, the suffix must be
promoted (e.g. 999999 -> '1.0 million' instead of '1000.0 thousand').
"""

import pytest

from alvo import intword


@pytest.mark.parametrize(
    "value, expected",
    [
        # The exact case from the issue report.
        (999999, "1.0 million"),
        # Same rounding-promotion bug at other power boundaries.
        (999999999, "1.0 billion"),
        (999_999_999_999, "1.0 trillion"),
        (999_999_999_999_999, "1.0 quadrillion"),
    ],
)
def test_rounding_promotes_suffix(value, expected):
    assert intword(value) == expected


def test_issue_example():
    assert intword(999999) == "1.0 million"


def test_rounding_promotes_with_custom_format():
    # The number is rendered with the requested format, but the unit must
    # still be promoted from "thousand" to "million".
    assert intword(999999, format="%.0f") == "1 million"
    assert intword(1_499_999, format="%.0f") == "1 million"
    assert intword(999999, format="%.2f") == "1.00 million"


def test_no_promotion_when_rounding_does_not_cross_boundary():
    # Sanity checks: values that must not be promoted.
    assert intword(999949) == "999.9 thousand"
    assert intword(1000000) == "1.0 million"
    assert intword(1500000) == "1.5 million"
    assert intword(1500) == "1.5 thousand"


def test_negative_promoted_value_keeps_sign():
    assert intword(-999999) == "-1.0 million"
    assert intword(-999999999) == "-1.0 billion"
