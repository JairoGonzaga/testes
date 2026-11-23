import pytest

from alvo import intword


def test_intword_1000_is_humanized():
    """Exactly 1000 must get the "thousand" suffix (was returned unchanged)."""
    assert intword(1000) == "1.0 thousand"


def test_intword_negative_1000_is_humanized():
    assert intword(-1000) == "-1.0 thousand"


def test_intword_other_exact_powers_are_humanized():
    assert intword(10**6) == "1.0 million"
    assert intword(10**9) == "1.0 billion"
    assert intword(-10**12) == "-1.0 trillion"


@pytest.mark.parametrize(
    "value,expected",
    [
        (999, "999"),
        (1001, "1.0 thousand"),
        (1500, "1.5 thousand"),
        (1000.0, "1.0 thousand"),
        ("1000", "1.0 thousand"),
    ],
)
def test_intword_boundary_values(value, expected):
    assert intword(value) == expected


def test_intword_rounding_into_next_unit_still_works():
    assert intword(999999) == "1.0 million"
    assert intword(10**6 - 1) == "1.0 million"


def test_non_finite_values_unchanged():
    assert intword(float("nan")) == "NaN"
    assert intword(float("inf")) == "+Inf"
    assert intword(float("-inf")) == "-Inf"
