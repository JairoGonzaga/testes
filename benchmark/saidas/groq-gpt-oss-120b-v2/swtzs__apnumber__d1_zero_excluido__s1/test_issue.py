import pytest
from alvo import apnumber


def test_zero_is_spelled_out():
    """Zero should be returned as the word 'zero'."""
    assert apnumber(0) == "zero"


def test_other_single_digit_behaviour_unchanged():
    """Other single‑digit numbers should still be spelled out."""
    assert apnumber(5) == "five"
