import pytest

from alvo import validate


def test_validate_standard_luhn_example():
    assert validate('79927398713') == '79927398713'
