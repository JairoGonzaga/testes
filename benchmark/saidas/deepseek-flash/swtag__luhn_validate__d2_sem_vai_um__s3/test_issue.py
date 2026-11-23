"""Reproduction tests for the Luhn checksum bug described in ISSUE.md.

The doubled digits must be summed as *digit sums* (`sum(divmod(d * 2, 10))`),
not as the raw doubled value reduced modulo the alphabet size.  With the buggy
implementation every number whose doubled digits include 5 or more is wrongly
rejected.
"""

import pytest

from alvo import InvalidChecksum, InvalidFormat, checksum, validate

# Standard, well known valid Luhn numbers (from the Luhn specification and the
# public test-card lists).  Each of them contains doubled digits >= 5.
VALID_NUMBERS = [
    "79927398713",  # the canonical example from the Luhn Wikipedia article
    "17893729974",
    "1234567812345670",
    "4111111111111111",
    "4012888888881881",
    "5555555555554444",
    "4242424242424242",
]

INVALID_NUMBERS = [
    "79927398710",
    "79927398711",
    "79927398712",
    "79927398714",
    "4242424242424241",
    "4111111111111112",
]


@pytest.mark.parametrize("number", VALID_NUMBERS)
def test_validate_accepts_valid_luhn_numbers(number):
    assert validate(number) == number


@pytest.mark.parametrize("number", VALID_NUMBERS)
def test_checksum_of_valid_numbers_is_zero(number):
    assert checksum(number) == 0


@pytest.mark.parametrize("number", INVALID_NUMBERS)
def test_validate_rejects_invalid_luhn_numbers(number):
    with pytest.raises(InvalidChecksum):
        validate(number)


def test_canonical_example_from_issue():
    # `validate('79927398713')` must return the number instead of raising.
    assert validate("79927398713") == "79927398713"


def test_checksum_handles_doubled_digits_above_four():
    # '18': digits from the right are ('8', '1'); the doubled '1' becomes 2,
    # so 8 + 2 = 10 -> checksum 0.
    assert checksum("18") == 0
    # '59': digits from the right are ('9', '5'); the doubled '5' becomes 10,
    # whose digit sum is 1, so 9 + 1 = 10 -> checksum 0 (the buggy version,
    # which keeps 10 instead of its digit sum, yields 9).
    assert checksum("59") == 0
    # '69': digits from the right are ('9', '6'); the doubled '6' becomes 12,
    # whose digit sum is 3, so 9 + 3 = 12 -> checksum 2 (buggy: (9 + 12) % 10 == 1).
    assert checksum("69") == 2


def test_validate_rejects_empty_number():
    with pytest.raises(InvalidFormat):
        validate("")


def test_validate_rejects_non_numeric_characters():
    with pytest.raises(InvalidFormat):
        validate("7992739871a")
