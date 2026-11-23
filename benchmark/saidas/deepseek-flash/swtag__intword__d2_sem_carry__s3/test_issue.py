"""Reproduction tests for ISSUE.md: intword(999999) returns '1000.0 thousand'.

When rounding (via the `format` string) pushes the chopped value up to 1000,
the suffix must be promoted to the next power (e.g. 'thousand' -> 'million')
instead of printing '1000.0 thousand'.
"""

import pytest

from alvo import human_powers, intword, powers


def test_issue_example_promotes_thousand_to_million():
    assert intword(999999) == "1.0 million"


@pytest.mark.parametrize(
    "value, expected",
    [
        (999_999, "1.0 million"),
        (999_999_999, "1.0 billion"),
        (999_999_999_999, "1.0 trillion"),
        (999_999_999_999_999, "1.0 quadrillion"),
    ],
)
def test_rounding_up_promotes_suffix(value, expected):
    assert intword(value) == expected


@pytest.mark.parametrize("exponent", [6, 9, 12, 15, 18])
def test_just_below_each_power_promotes_to_that_power(exponent):
    """10**e - 1 rounds up to 1000 units of 10**(e-1), i.e. 1 of 10**e."""
    unit = human_powers[powers.index(10**exponent)]
    assert intword(10**exponent - 1) == "1.0 " + unit


def test_promotion_keeps_negative_prefix():
    assert intword(-999_999) == "-1.0 million"
    assert intword(-(10**9) + 1) == "-1.0 billion"


def test_promotion_respects_format_string():
    assert intword(999_999, "%.0f") == "1 million"
    assert intword(999_999, "%.2f") == "1.00 million"


def test_values_that_do_not_round_up_are_unchanged():
    assert intword(999) == "999"
    assert intword(1000) == "1.0 thousand"
    assert intword(1500) == "1.5 thousand"
    assert intword(9_994_999) == "10.0 million"
    assert intword(999_499_999) == "999.5 million"


@pytest.mark.parametrize("exponent", [6, 9, 12, 15, 18])
@pytest.mark.parametrize("delta", [1, 2, 10, 500])
def test_mantissa_never_reaches_1000_when_bigger_suffix_exists(exponent, delta):
    """A result must never be reported as e.g. '1000.0 thousand'."""
    value = 10**exponent - delta
    result = intword(value)
    mantissa, unit = result.split(" ", 1)
    assert unit in human_powers, (value, result)
    assert float(mantissa) < 1000, (value, result)


def test_top_power_is_not_promoted_past_googol():
    assert intword(10**100) == "1.0 googol"
    assert intword(10**101) == "10.0 googol"
    # No suffix exists beyond 'googol', so nothing can be promoted there.
    assert intword(999 * 10**100) == "999.0 googol"


def test_powers_and_units_stay_aligned():
    assert len(powers) == len(human_powers)
