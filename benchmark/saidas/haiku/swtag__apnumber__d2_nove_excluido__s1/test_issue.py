import pytest

from alvo import apnumber


def test_nine_is_spelled_out():
    # Issue: apnumber(9) returned '9' instead of 'nine'.
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
def test_all_single_digits_are_spelled_out(value, expected):
    assert apnumber(value) == expected


def test_ten_is_still_returned_as_digits():
    # Boundary check: only single-digit values are spelled out.
    assert apnumber(10) == "10"
