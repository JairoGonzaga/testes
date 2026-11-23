import pytest

from alvo import intword


def test_issue_999999_promotes_to_million():
    # Reported bug: returns '1000.0 thousand' instead of '1.0 million'.
    assert intword(999999) == "1.0 million"


@pytest.mark.parametrize(
    "value, expected",
    [
        (-999999, "-1.0 million"),
        (999999999, "1.0 billion"),
        (999999999999, "1.0 trillion"),
    ],
)
def test_rounding_up_promotes_suffix_to_next_power(value, expected):
    assert intword(value) == expected


def test_no_promotion_when_rounding_stays_below_next_power():
    assert intword(999400) == "999.4 thousand"
