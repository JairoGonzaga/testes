import pytest

from alvo import apnumber


def test_zero_is_spelled_out():
    """The issue: apnumber(0) should return the word 'zero', not '0'."""
    assert apnumber(0) == "zero"


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
    """Docs say numbers from 0 to 9 are returned as words."""
    assert apnumber(value) == expected
