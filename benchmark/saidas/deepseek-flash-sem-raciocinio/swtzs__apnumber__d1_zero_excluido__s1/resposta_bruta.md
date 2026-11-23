```python
import pytest

from alvo import apnumber


def test_apnumber_zero_returns_zero_word():
    assert apnumber(0) == "zero"


def test_apnumber_single_digits_spelled_out():
    assert apnumber(5) == "five"
    assert apnumber(9) == "nine"


def test_apnumber_zero_float_returns_zero_word():
    assert apnumber(0.0) == "zero"


def test_apnumber_out_of_range_returns_digits():
    assert apnumber(10) == "10"
    assert apnumber(-1) == "-1"
```