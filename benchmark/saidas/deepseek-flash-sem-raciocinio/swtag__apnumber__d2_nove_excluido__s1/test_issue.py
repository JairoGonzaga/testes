import pytest

from alvo import apnumber


def test_apnumber_nine_returns_word():
    """apnumber(9) should spell out 'nine', not return the digit '9'."""
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
def test_apnumber_all_single_digits_spelled_out(value, expected):
    """Every single digit from 0 through 9 must be spelled out."""
    assert apnumber(value) == expected


def test_apnumber_nine_from_float_and_string():
    """9 given as a float or a string should also render as 'nine'."""
    assert apnumber(9.0) == "nine"
    assert apnumber("9") == "nine"


def test_apnumber_double_digits_stay_digits():
    """Numbers outside 0..9 are still returned as digits (no regression)."""
    assert apnumber(10) == "10"
    assert apnumber(-1) == "-1"
