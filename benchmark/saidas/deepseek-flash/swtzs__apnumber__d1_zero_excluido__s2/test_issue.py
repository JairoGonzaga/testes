import pytest

from alvo import apnumber


@pytest.mark.parametrize(
    "value, expected",
    [
        (0, "zero"),
        (0.0, "zero"),
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
def test_apnumber_spells_out_single_digits(value, expected):
    assert apnumber(value) == expected
