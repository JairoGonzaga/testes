```python
import pytest

from alvo import validate


def test_luhn_textbook_example_valid():
    # 79927398713 is the classic valid Luhn example.
    assert validate('79927398713') == '79927398713'


def test_luhn_other_valid_numbers():
    # Additional known-valid Luhn numbers.
    assert validate('4539148803436467') == '4539148803436467'
    assert validate('79927398710')  # placeholder removed below
```