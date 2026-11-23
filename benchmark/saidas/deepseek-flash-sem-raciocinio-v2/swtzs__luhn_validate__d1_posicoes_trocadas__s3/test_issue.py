import pytest

from alvo import validate


def test_validate_textbook_luhn_number_returns_number():
    assert validate('79927398713') == '79927398713'


def test_validate_textbook_luhn_number_does_not_raise_invalid_checksum():
    from alvo import InvalidChecksum
    try:
        assert validate('79927398713') == '79927398713'
    except InvalidChecksum:
        pytest.fail("valid Luhn number was rejected with InvalidChecksum")
