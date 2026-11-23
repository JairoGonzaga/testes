import pytest

from alvo import apnumber


@pytest.mark.parametrize(
    ("value", "expected"),
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


def test_issue_apnumber_nine_returns_nine_word():
    # Reported bug: apnumber(9) returned '9' instead of 'nine'.
    assert apnumber(9) == "nine"


def test_numbers_from_ten_up_stay_as_digits():
    assert apnumber(10) == "10"
    assert apnumber(42) == "42"
