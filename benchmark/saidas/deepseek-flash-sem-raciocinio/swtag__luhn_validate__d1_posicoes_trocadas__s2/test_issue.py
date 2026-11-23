import pytest

from alvo import validate, checksum, InvalidChecksum, InvalidFormat


def test_textbook_luhn_number_is_valid():
    assert validate('79927398713') == '79927398713'


def test_textbook_luhn_number_checksum_zero():
    assert checksum('79927398713') == 0


@pytest.mark.parametrize('number', [
    '79927398713',
    '49927398716',
    '1234567812345670',
    '0',
    '18',
    '4532015112830366',
])
def test_other_valid_luhn_numbers(number):
    assert validate(number) == number


@pytest.mark.parametrize('number', [
    '79927398710',
    '79927398711',
    '79927398712',
    '79927398714',
    '49927398717',
    '1234567812345678',
])
def test_invalid_luhn_numbers_rejected(number):
    with pytest.raises(InvalidChecksum):
        validate(number)


def test_empty_is_invalid_format():
    with pytest.raises(InvalidFormat):
        validate('')


def test_non_digit_is_invalid_format():
    with pytest.raises(InvalidFormat):
        validate('7992739871a')
