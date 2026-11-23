"""Tests reproducing the issue: valid Luhn numbers are rejected."""

import pytest

from alvo import InvalidChecksum, checksum, validate


# Textbook Luhn example: the check digit of 7992739871 is 3, so the full
# number 79927398713 has a valid Luhn check digit and must be accepted.
TEXTBOOK_NUMBER = "79927398713"

# Other numbers that satisfy the standard Luhn algorithm
# (doubling every second digit starting from the rightmost-but-one digit).
VALID_NUMBERS = [
    "79927398713",       # textbook example (Wikipedia)
    "49927398716",       # second Wikipedia example
    "4111111111111111",  # common test Visa number
    "5500005555555559",  # common test MasterCard number
    "6011111111111117",  # common test Discover number
    "378282246310005",   # common test American Express number
    "4222222222222",     # common test Visa number
    "18",                # smallest positive valid number
    "0",                 # zero is a valid Luhn number
]

# Numbers whose check digit is wrong according to the standard Luhn algorithm.
INVALID_NUMBERS = [
    "79927398710",
    "79927398711",
    "79927398712",
    "49927398717",
    "4111111111111112",
]


def test_textbook_luhn_number_is_returned():
    """The textbook valid number must be returned unchanged by validate()."""
    assert validate(TEXTBOOK_NUMBER) == TEXTBOOK_NUMBER


def test_textbook_luhn_number_has_zero_checksum():
    assert checksum(TEXTBOOK_NUMBER) == 0


@pytest.mark.parametrize("number", VALID_NUMBERS)
def test_valid_numbers_pass_validate(number):
    assert validate(number) == number


@pytest.mark.parametrize("number", VALID_NUMBERS)
def test_valid_numbers_have_zero_checksum(number):
    assert checksum(number) == 0


@pytest.mark.parametrize("number", INVALID_NUMBERS)
def test_invalid_numbers_raise_invalid_checksum(number):
    with pytest.raises(InvalidChecksum):
        validate(number)


@pytest.mark.parametrize("number", INVALID_NUMBERS)
def test_invalid_numbers_have_nonzero_checksum(number):
    assert checksum(number) != 0


def test_checksum_differs_for_wrong_check_digit():
    """Changing the check digit of a valid number must change the checksum."""
    assert checksum("79927398713") == 0
    assert checksum("79927398710") != 0
