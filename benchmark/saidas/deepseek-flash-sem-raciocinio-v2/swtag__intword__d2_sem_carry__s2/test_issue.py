import pytest

from alvo import intword


def test_example_from_issue():
    assert intword(999999) == "1.0 million"


@pytest.mark.parametrize(
    "value, expected",
    [
        (999999, "1.0 million"),
        (999999999, "1.0 billion"),
        (999999999999, "1.0 trillion"),
        (-999999, "-1.0 million"),
        (-999999999, "-1.0 billion"),
    ],
)
def test_promotion_when_rounding_reaches_next_power(value, expected):
    assert intword(value) == expected


def test_no_promotion_when_rounding_stays_below_next_power():
    assert intword(999499) == "999.5 thousand"
    assert intword(998999999) == "999.0 million"
