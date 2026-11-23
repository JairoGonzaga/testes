import pytest

from alvo import InvalidChecksum, validate


def test_issue_example_is_accepted():
    # Standard Luhn example. On the current code it raises InvalidChecksum because
    # doubled digits >= 5 are reduced with mod 10 instead of summing the digits of 2*d.
    assert validate('79927398713') == '79927398713'


@pytest.mark.parametrize('number', [
    '59',
    '67',
    '75',
    '83',
    '91',
    '4539148803436467',
])
def test_valid_numbers_with_large_doubled_digits_are_accepted(number):
    assert validate(number) == number


@pytest.mark.parametrize('number', [
    '58',
    '79927398710',
])
def test_invalid_numbers_are_still_rejected(number):
    with pytest.raises(InvalidChecksum):
        validate(number)
