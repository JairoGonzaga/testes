import pytest

from alvo import apnumber


def test_zero_is_spelled_out():
    # Issue: apnumber(0) returns '0' instead of 'zero'.
    assert apnumber(0) == "zero"


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        (1, "one"),
        (2, "two"),
        (3, "three"),
        (4, "four"),
        (5, "five"),
        (6, "six"),
        (7, "seven"),
        (8, "eight"),
        (9, "nine"),
    ],
)
def test_single_digits_are_spelled_out(value, expected):
    assert apnumber(value) == expected


def test_ten_is_not_spelled_out():
    assert apnumber(10) == "10"
