# test_issue.py
import pytest
from alvo import apnumber


def test_single_digit_9_returns_word():
    """
    The bug is that apnumber(9) incorrectly returns the digit '9'
    instead of the word 'nine'.  The test will fail until the
    implementation uses the correct upper bound (10).
    """
    assert apnumber(9) == "nine"


def test_other_single_digits_are_spelled():
    """
    Verify that other single digits are spelled correctly.
    These cases already pass, but they reinforce the intended behaviour.
    """
    assert apnumber(0) == "zero"
    assert apnumber(4) == "four"
    assert apnumber(8) == "eight"


def test_multi_digit_numbers_are_not_spelled():
    """
    Numbers outside the 0–9 range should be returned unchanged as a string.
    """
    assert apnumber(10) == "10"
    assert apnumber(123) == "123"
