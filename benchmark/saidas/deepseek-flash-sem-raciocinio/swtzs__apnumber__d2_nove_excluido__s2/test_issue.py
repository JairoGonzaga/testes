import pytest
from alvo import apnumber


def test_apnumber_nine_spelled_out():
    assert apnumber(9) == "nine"


@pytest.mark.parametrize(
    "value,expected",
    [
        (0, "zero"),
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
def test_apnumber_single_digits_spelled_out(value, expected):
    assert apnumber(value) == expected


def test_apnumber_two_digits_stay_digits():
    assert apnumber(10) == "10"
    assert apnumber(42) == "42"
