"""Reproduction tests for the issue:

    intword(10**100) does not return '1.0 googol'

A googol (10**100) is the largest unit known by ``intword``.  When a value is
just below a unit boundary, ``intword`` rounds it and promotes it to the next
unit name (e.g. ``intword(999999)`` -> ``'1.0 million'``).  That promotion check
is done on ``float`` values, which cannot represent ``10**67`` exactly, so the
boundary-crossing detection breaks for the ``decillion`` -> ``googol`` step
(a factor of ``10**67``).  As a result ``intword(10**100)`` renders a mangled
(floating point rounded) number of decillions instead of ``'1.0 googol'``.
"""

import pytest

from alvo import intword


# ---------------------------------------------------------------------------
# The behaviour reported in the issue
# ---------------------------------------------------------------------------
def test_googol_is_humanized_as_one_googol():
    assert intword(10**100) == "1.0 googol"


def test_negative_googol_is_humanized_as_one_googol():
    assert intword(-(10**100)) == "-1.0 googol"


@pytest.mark.parametrize(
    "value",
    [
        10**100 - 1,        # one decillion away from a googol
        10**100 - 10**66,   # still rounds up to a whole googol
    ],
)
def test_values_just_below_googol_round_up_to_googol(value):
    assert intword(value) == "1.0 googol"


def test_googol_honours_the_format_argument():
    assert intword(10**100, format="%.2f") == "1.00 googol"


# ---------------------------------------------------------------------------
# Behaviour that must keep working (sanity checks, these pass before and after)
# ---------------------------------------------------------------------------
@pytest.mark.parametrize(
    "value,expected",
    [
        (999, "999"),
        (1500, "1.5 thousand"),
        (-1500, "-1.5 thousand"),
        (999999, "1.0 million"),
        (10**36, "1000.0 decillion"),
        (2 * 10**100, "2.0 googol"),
        (10**101, "10.0 googol"),
        (float("nan"), "NaN"),
        (float("-inf"), "-Inf"),
        ("not a number", "not a number"),
    ],
)
def test_existing_behaviour_is_unchanged(value, expected):
    assert intword(value) == expected
