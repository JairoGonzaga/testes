"""Tests reproducing the issue: valid Luhn numbers are rejected.

The module doubles the wrong set of digits (it doubles the digits at even
positions counted from the *right* instead of every second digit starting
with the second-to-last one), so textbook-valid Luhn numbers such as
'79927398713' raise InvalidChecksum.
"""

import pytest

from alvo import checksum, validate
from alvo import InvalidChecksum, InvalidFormat, ValidationError


VALID_NUMBERS = [
    "79927398713",  # textbook Luhn example from the issue
    "49927398716",
    "1234567812345670",
    "4111111111111111",
    "5500005555555559",
    "378282246310005",  # American Express test number
    "6011111111111117",  # Discover test number
    "30569309025904",  # Diners Club test number
]

INVALID_NUMBERS = [
    "79927398710",
    "79927398711",
    "79927398712",
    "49927398717",
    "4111111111111112",
    "1234567812345678",
]


@pytest.mark.parametrize("number", VALID_NUMBERS)
def test_checksum_of_valid_number_is_zero(number):
    assert checksum(number) == 0


@pytest.mark.parametrize("number", VALID_NUMBERS)
def test_validate_accepts_valid_number(number):
    assert validate(number) == number


@pytest.mark.parametrize("number", INVALID_NUMBERS)
def test_checksum_of_invalid_number_is_not_zero(number):
    assert checksum(number) != 0


@pytest.mark.parametrize("number", INVALID_NUMBERS)
def test_validate_rejects_invalid_checksum(number):
    with pytest.raises(InvalidChecksum):
        validate(number)


def test_issue_example():
    """Exactly the example reported in ISSUE.md."""
    assert validate("79927398713") == "79927398713"


def test_answer_does_not_trim_or_alter_the_number():
    number = "79927398713"
    assert validate(number) == number


def test_invalid_characters_still_raise_invalid_format():
    with pytest.raises(InvalidFormat):
        validate("7992739871x")
    assert issubclass(InvalidFormat, ValidationError)


def test_empty_number_still_raises_invalid_format():
    with pytest.raises(InvalidFormat):
        validate("")
