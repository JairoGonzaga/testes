"""Tests reproducing the Luhn bug described in ISSUE.md.

Valid numbers are rejected when a doubled digit is 5 or greater, because the
doubling step uses ``(digit * 2) % 10`` instead of adding the decimal digits of
the doubled value (``1 + (digit * 2 - 10)`` for values above 9).
"""

import pytest

from alvo import checksum, validate, InvalidChecksum, InvalidFormat


ALPHABET = "0123456789"


def luhn_checksum(number, alphabet=ALPHABET):
    """Reference (correct) Luhn checksum implementation."""
    n = len(alphabet)
    values = [alphabet.index(c) for c in reversed(str(number))]
    total = 0
    for i, value in enumerate(values):
        if i % 2 == 1:
            high, low = divmod(value * 2, n)
            total += high + low
        else:
            total += value
    return total % n


def make_valid(base, alphabet=ALPHABET):
    """Append the check digit that makes ``base`` a valid Luhn number."""
    n = len(alphabet)
    for check in alphabet:
        candidate = str(base) + check
        if luhn_checksum(candidate, alphabet) == 0:
            return candidate
    raise AssertionError("could not build a valid number from %r" % (base,))


# '79927398713' is the canonical valid Luhn number from the issue.
CANONICAL = "79927398713"

# Bases (without check digit) chosen so that a digit >= 5 lands in a doubled
# position, which is exactly the situation the buggy code gets wrong.
BASES_WITH_LARGE_DOUBLED_DIGITS = [
    "7992739871",   # -> 79927398713, the example from the issue
    "7",
    "9",
    "59",
    "699",
    "9876",
    "1234567890",
    "55555555",
    "6789",
    "90909090",
]


def test_canonical_valid_number_is_accepted():
    assert validate(CANONICAL) == CANONICAL


def test_canonical_checksum_is_zero():
    assert checksum(CANONICAL) == 0


@pytest.mark.parametrize("base", BASES_WITH_LARGE_DOUBLED_DIGITS)
def test_valid_numbers_with_large_doubled_digits_are_accepted(base):
    number = make_valid(base)
    # Sanity check: this number really is valid per the reference algorithm.
    assert luhn_checksum(number) == 0
    assert validate(number) == number


@pytest.mark.parametrize(
    "number", ["79927398710", "79927398711", "79927398712", "79927398714"]
)
def test_numbers_with_wrong_check_digit_are_rejected(number):
    assert luhn_checksum(number) != 0
    with pytest.raises(InvalidChecksum):
        validate(number)


def test_checksum_matches_reference_for_canonical_number():
    assert checksum(CANONICAL) == luhn_checksum(CANONICAL)


@pytest.mark.parametrize(
    "number",
    ["0", "18", "26", "59", "0000000000", "4242424242424242", "4111111111111111"],
)
def test_checksum_matches_reference(number):
    assert checksum(number) == luhn_checksum(number)
    assert validate(number) == number


def test_empty_number_is_invalid_format():
    with pytest.raises(InvalidFormat):
        validate("")
