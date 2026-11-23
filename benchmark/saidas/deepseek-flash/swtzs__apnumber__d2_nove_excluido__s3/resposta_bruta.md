```python
import pytest

from alvo import apnumber


@pytest.mark.parametrize(
    "number, expected",
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
def test_single_digit_numbers_are_spelled_out(number, expected):
    assert apnumber(number) == expected


def test_apnumber_9_regression():
    assert apnumber(9) == "nine"
```