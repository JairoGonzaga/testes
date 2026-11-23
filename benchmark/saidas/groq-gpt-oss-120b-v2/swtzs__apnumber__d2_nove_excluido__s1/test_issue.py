import pytest
from alvo import apnumber


def test_single_digit_numbers_spelled_out():
    # Numbers 0‑9 should be returned as words
    assert apnumber(0) == "zero"
    assert apnumber(5) == "five"
    assert apnumber(8) == "eight"
    # Bug: 9 should be spelled out but currently returns "9"
    assert apnumber(9) == "nine"
