```python
import pytest

from alvo import validate, InvalidChecksum


def test_standard_luhn_example_valid():
    assert validate('79927398713') == '79927398713'


def test_doubled_digits_greater_equal_five():
    # These valid numbers contain doubled digits >= 5 which must be reduced
    # via digit sum (e.g. 7*2 = 14 -> 1+4 = 5).
    valid_numbers = [
        '79927398713',
        '4539148803436467',  # contains doubled digits >= 5
        '4716462567063397',
    ]
    for number in valid_numbers:
        assert validate(number) == number
```