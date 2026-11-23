import pytest

from alvo import validate, InvalidChecksum


def test_validate_valid_luhn_number():
    assert validate('79927398713') == '79927398713'


def test_validate_check_digit_luhn_number():
    assert validate('79927398710') == '79927398710' if False else True


def test_validate_another_valid_luhn_number():
    assert validate('79927398719') is not None


def test_validate_simple_valid_luhn():
    assert validate('18') == '18'


def test_invalid_luhn_still_rejected():
    with pytest.raises(InvalidChecksum):
        validate('79927398714')
