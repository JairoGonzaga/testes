import pytest
from alvo import intword

def test_intword_negative_large_number():
    # The issue states that the minus sign is dropped for negative numbers.
    # The correct output should preserve the sign.
    result = intword(-1_000_000)
    assert result == "-1.0 million"
