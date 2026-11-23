import pytest

from alvo import intword


def test_rounding_promotes_suffix():
    """The exact case from the issue report."""
    assert intword(999999) == "1.0 million"


def test_rounding_promotes_suffix_negative():
    assert intword(-999999) == "-1.0 million"


@pytest.mark.parametrize(
    "value,expected",
    [
        (999999, "1.0 million"),
        (999999999, "1.0 billion"),
        (999999999999, "1.0 trillion"),
        (999999999999999, "1.0 quadrillion"),
        (999999999999999999, "1.0 quintillion"),
    ],
)
def test_rounding_promotion_various_scales(value, expected):
    assert intword(value) == expected


def test_no_promotion_when_not_needed():
    assert intword(1000) == "1.0 thousand"
    assert intword(1234) == "1.2 thousand"
    assert intword(1500000) == "1.5 million"
    assert intword(999999999999) != "1000.0 thousand"
