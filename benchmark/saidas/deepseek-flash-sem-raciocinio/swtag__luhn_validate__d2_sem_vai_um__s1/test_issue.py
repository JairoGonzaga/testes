import pytest

from alvo import validate, checksum, InvalidChecksum, InvalidFormat


def test_standard_luhn_example_is_valid():
    assert validate('79927398713') == '79927398713'


def test_checksum_zero_for_standard_example():
    assert checksum('79927398713') == 0


@pytest.mark.parametrize('number', [
    '79927398713',
    '49927398716',
    '1234567812345670',
    '0',
    '18',
])
def test_valid_numbers_accepted(number):
    assert validate(number) == number


@pytest.mark.parametrize('number', [
    '79927398710',
    '79927398714',
    '49927398717',
    '1234567812345678',
])
def test_invalid_numbers_rejected(number):
    with pytest.raises(InvalidChecksum):
        validate(number)


def test_empty_rejected():
    with pytest.raises(InvalidFormat):
        validate('')
