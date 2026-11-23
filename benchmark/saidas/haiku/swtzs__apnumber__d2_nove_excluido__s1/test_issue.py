import pytest

from alvo import apnumber


def test_apnumber_nine_is_spelled_out():
    assert apnumber(9) == "nine"


@pytest.mark.parametrize(
    "value, expected",
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
def test_single_digit_numbers_are_spelled_out(value, expected):
    assert apnumber(value) == expected


def test_two_digit_numbers_are_returned_as_digits():
    assert apnumber(10) == "10"
