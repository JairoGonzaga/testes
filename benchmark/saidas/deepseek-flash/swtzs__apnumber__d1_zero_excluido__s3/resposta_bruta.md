```python
import pytest

from alvo import apnumber


DIGIT_WORDS = [
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
]


@pytest.mark.parametrize("value, expected", DIGIT_WORDS)
def test_apnumber_spells_out_single_digits(value, expected):
    assert apnumber(value) == expected


def test_apnumber_zero_is_spelled_out():
    assert apnumber(0) == "zero"


@pytest.mark.parametrize("value", [-10, -1, 10, 11, 100])
def test_apnumber_leaves_numbers_outside_single_digit_range_as_strings(value):
    assert apnumber(value) == str(value)
```