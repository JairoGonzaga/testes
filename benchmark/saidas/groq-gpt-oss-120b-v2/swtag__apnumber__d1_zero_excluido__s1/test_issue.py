import pytest
from alvo import apnumber

def test_zero_is_spelled_out():
    # According to the documentation, zero should be returned as the word "zero".
    assert apnumber(0) == "zero"

def test_other_single_digits_remain_unchanged():
    # Ensure that other single-digit numbers still return their word forms.
    assert apnumber(5) == "five"
    assert apnumber(9) == "nine"
