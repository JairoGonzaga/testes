import pytest
from alvo import validate

def test_standard_luhn_valid():
    """The classic Luhn example should be accepted and returned unchanged."""
    assert validate("79927398713") == "79927398713"
