# test_issue.py
import pytest
from alvo import validate, InvalidFormat, InvalidChecksum


def test_validate_returns_same_int_when_valid():
    """
    validate() should return the input integer unchanged when the checksum is valid.
    """
    number = 79927398713
    result = validate(number)
    assert result == number
    assert isinstance(result, int)


def test_validate_returns_same_str_when_valid():
    """
    validate() should return the input string unchanged when the checksum is valid.
    """
    number = "79927398713"
    result = validate(number)
    assert result == number
    assert isinstance(result, str)
