"""Reproduction tests for the issue: ``intword(10**100)`` must return ``'1.0 googol'``.

The bug: ``intword`` divides the (exact) integer value by the current power in
floating point arithmetic.  For 10**100 the code first lands on the "decillion"
(10**33) suffix, so ``value / power`` becomes ``1e67``, which is not exactly
representable as a float.  The "round up to the next suffix" check then compares
that lossy float against the exact integer ``10**100 // 10**33`` and fails, so
instead of promoting the number to ``googol`` the function formats the float
artefact into a 67 digit decillion amount.
"""

import pytest

from alvo import intword


def test_intword_googol():
    """The exact case from the issue report."""
    assert intword(10**100) == "1.0 googol"


def test_intword_googol_uses_googol_suffix():
    """The googol suffix must be used instead of a huge decillion amount."""
    result = intword(10**100)
    assert result.endswith("googol")
    assert "decillion" not in result


def test_intword_googol_has_no_float_artefacts():
    """No lossy float digits may leak into the formatted number."""
    result = intword(10**100)
    number = result.split(" ")[0]
    # The float closest to 1e67 expands to these digits; they must not appear.
    assert "9999999999999999827367757839185598317239782875580932278577147150336" not in number
    assert len(number.replace(".", "")) <= 4


def test_intword_negative_googol():
    assert intword(-(10**100)) == "-1.0 googol"


def test_intword_googol_from_string():
    """Strings are coerced to int, so this must behave like the int input."""
    assert intword(str(10**100)) == "1.0 googol"


@pytest.mark.parametrize(
    "value, expected",
    [
        (2 * 10**100, "2.0 googol"),
        (10 * 10**100, "10.0 googol"),
        (10**101, "10.0 googol"),
        (15 * 10**99, "1.5 googol"),
        (999 * 10**99, "99.9 googol"),
        (-3 * 10**100, "-3.0 googol"),
        # Behaviour that is already correct must be preserved.
        (10**33, "1.0 decillion"),
        (10**30, "1.0 nonillion"),
        (1234567, "1.2 million"),
        (10**6, "1.0 million"),
        (999, "999"),
    ],
)
def test_intword_existing_behaviour_preserved(value, expected):
    assert intword(value) == expected
