import pytest

from alvo import checksum, validate

# Numbers with a valid Luhn check digit (the textbook example and well-known
# published test numbers). Each one is rejected by the current code.
VALID_LUHN_NUMBERS = [
    '79927398713',
    '4111111111111111',
    '378282246310005',
    '4539578763621486',
    '1234567812345670',
]


def test_issue_textbook_luhn_example_is_accepted():
    assert validate('79927398713') == '79927398713'


@pytest.mark.parametrize('number', VALID_LUHN_NUMBERS)
def test_valid_luhn_numbers_are_accepted(number):
    assert validate(number) == number


@pytest.mark.parametrize('number', VALID_LUHN_NUMBERS)
def test_checksum_of_valid_luhn_number_is_zero(number):
    assert checksum(number) == 0
