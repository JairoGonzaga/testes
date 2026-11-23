import pytest

from alvo import intword


def test_intword_promotes_suffix_when_rounding_reaches_next_power():
    # Issue: intword(999999) returned '1000.0 thousand' instead of '1.0 million'.
    assert intword(999999) == "1.0 million"


@pytest.mark.parametrize(
    "value, expected",
    [
        (999999, "1.0 million"),
        (-999999, "-1.0 million"),
        (999999999, "1.0 billion"),
        (-999999999, "-1.0 billion"),
    ],
)
def test_intword_promotes_suffix_for_rounding_overflow(value, expected):
    assert intword(value) == expected
