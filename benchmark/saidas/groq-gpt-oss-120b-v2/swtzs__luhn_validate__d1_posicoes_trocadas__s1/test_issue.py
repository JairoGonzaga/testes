import pytest
from alvo import validate

def test_luhn_example_is_accepted():
    """The textbook Luhn number must be considered valid."""
    result = validate('79927398713')
    assert result == '79927398713'
