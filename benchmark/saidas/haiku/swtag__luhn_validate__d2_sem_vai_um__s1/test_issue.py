import pytest

from alvo import InvalidChecksum, validate


def test_standard_luhn_example_is_accepted():
    # 79927398713 is the standard valid Luhn example. Its doubled digits
    # include values >= 5 (e.g. 9 doubled to 18), which the checksum mishandles.
    assert validate('79927398713') == '79927398713'


@pytest.mark.parametrize('number', [
    '79927398713',
    '5555555555554444',
    '5105105105105100',
])
def test_valid_numbers_with_large_doubled_digits_are_accepted(number):
    assert validate(number) == number


def test_checksum_error_still_raised_for_invalid_number():
    # Changing only the last digit of the valid example breaks the checksum.
    with pytest.raises(InvalidChecksum):
        validate('79927398710')
