import pytest

from alvo import validate


def test_textbook_luhn_number_is_valid():
    assert validate('79927398713') == '79927398713'
