import pytest
from alvo import intword

def test_intword_googol():
    """
    A googol (10**100) must be rendered as '1.0 googol'.
    The current buggy implementation returns a decillion string,
    so this test fails until the issue is fixed.
    """
    assert intword(10**100) == "1.0 googol"
