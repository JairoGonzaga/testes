# test_issue.py
import pytest
from alvo import validate, InvalidChecksum

def test_valid_luhn_number_is_accepted():
    """The textbook Luhn example must pass validation."""
    assert validate('79927398713') == '79927398713'
