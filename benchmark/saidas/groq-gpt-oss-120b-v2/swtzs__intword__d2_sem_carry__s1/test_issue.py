import pytest
from alvo import intword


def test_intword_rounded_up_to_next_power():
    """
    Verify that rounding a number that reaches the next power promotes the suffix.

    Input: 999999
    Expected output (as stated in the issue): "1.0 million"
    """
    assert intword(999999) == "1.0 million"
