import pytest
from alvo import intword


def test_intword_rounding_promotion_positive():
    """
    The function should promote to the next unit when rounding pushes a value
    exactly to the power threshold. For 999_999, the rounded value is 1000.0,
    which equals the power 1_000. The expected result is '1.0 million'.
    """
    assert intword(999999) == "1.0 million"
