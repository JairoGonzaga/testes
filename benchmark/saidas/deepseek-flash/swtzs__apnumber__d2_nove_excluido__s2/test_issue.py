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
def test_apnumber_spells_out_single_digit_numbers(value, expected):
    assert apnumber(value) == expected


def test_apnumber_9_returns_nine_not_digit():
    assert apnumber(9) == "nine"
    assert apnumber(9) != "9"
