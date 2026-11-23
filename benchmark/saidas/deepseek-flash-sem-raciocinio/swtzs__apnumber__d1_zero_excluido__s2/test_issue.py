import pytest
from alvo import apnumber


def test_apnumber_zero_is_spelled_out():
    assert apnumber(0) == "zero"


@pytest.mark.parametrize(
    "value, expected",
    [
        (0, "zero"),
        (1, "one"),
        (5, "five"),
        (9, "nine"),
    ],
)
def test_apnumber_single_digits_are_words(value, expected):
    assert apnumber(value) == expected
