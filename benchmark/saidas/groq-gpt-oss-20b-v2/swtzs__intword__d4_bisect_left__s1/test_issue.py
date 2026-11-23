# test_issue.py
import pytest
from alvo import intword

def test_googol_is_correctly_humanized():
    """
    intword(10**100) should return '1.0 googol'.
    With the current buggy implementation it returns a huge decillion string,
    so the test fails.  After the bug is fixed the test passes.
    """
    assert intword(10**100) == "1.0 googol"
