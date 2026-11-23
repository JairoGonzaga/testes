import pytest

from alvo import validate, checksum, InvalidChecksum


def test_validate_standard_luhn_number():
    assert validate('79927398713') == '79927398713'


def test_checksum_standard_luhn_number():
    assert checksum('79927398713') == 0


def test_validate_another_number_with_large_doubled_digits():
    # 4111111111111111 is a well-known valid Luhn test card number.
    assert validate('4111111111111111') == '4111111111111111'


def test_invalid_number_still_raises():
    with pytest.raises(InvalidChecksum):
        validate('79927398710')
