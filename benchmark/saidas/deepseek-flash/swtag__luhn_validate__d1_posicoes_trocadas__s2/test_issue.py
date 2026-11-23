"""Reproduction tests for the issue "Valid Luhn number rejected".

The textbook Luhn example number ``79927398713`` is a valid Luhn number
(check digit 3) but ``alvo.validate`` rejects it with ``InvalidChecksum``.
"""

import pytest

from alvo import InvalidChecksum, InvalidFormat, checksum, validate


# Numbers that are valid according to the Luhn algorithm.
# The parity of the digits that get doubled must be computed from the
# rightmost digit (the check digit is never doubled).
VALID_LUHN_NUMBERS = [
    "79927398713",      # the textbook example from the issue
    "4111111111111111",  # classic Visa test number
    "4242424242424242",  # classic Visa test number
    "1234567812345670",
    "18",
    "26",
]

# Numbers that are NOT valid Luhn numbers under either doubling convention
# (so they must always be rejected, whatever the parity used).
INVALID_LUHN_NUMBERS = [
    "79927398710",
    "79927398711",
    "79927398714",
    "4111111111111112",
    "4242424242424241",
    "1234567812345671",
]


@pytest.mark.parametrize("number", VALID_LUHN_NUMBERS)
def test_validate_accepts_valid_luhn_number(number):
    assert validate(number) == number


@pytest.mark.parametrize("number", VALID_LUHN_NUMBERS)
def test_checksum_of_valid_luhn_number_is_zero(number):
    assert checksum(number) == 0


def test_textbook_example_from_issue():
    # Exact scenario reported in ISSUE.md: this must not raise.
    assert validate("79927398713") == "79927398713"


@pytest.mark.parametrize("number", INVALID_LUHN_NUMBERS)
def test_validate_rejects_invalid_luhn_number(number):
    with pytest.raises(InvalidChecksum):
        validate(number)


def test_validate_still_rejects_non_numeric_input():
    with pytest.raises(InvalidFormat):
        validate("7992739871x")
