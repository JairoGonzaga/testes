import pytest

from alvo import InvalidChecksum, InvalidFormat, validate


def test_issue_example_is_valid():
    # Doubled digits 8 and 9 (giving 16 and 18) must be reduced to digit sums.
    assert validate('79927398713') == '79927398713'


@pytest.mark.parametrize(
    'number',
    [
        '79927398713',
        '5555555555554444',
        '378282246310005',
    ],
)
def test_valid_numbers_with_large_doubled_digits_are_accepted(number):
    assert validate(number) == number


def test_wrong_check_digit_is_rejected():
    with pytest.raises(InvalidChecksum):
        validate('79927398710')


def test_empty_input_is_invalid_format():
    with pytest.raises(InvalidFormat):
        validate('')


def test_non_digit_input_is_invalid_format():
    with pytest.raises(InvalidFormat):
        validate('7992x398713')
