"""Reproduces the issue "Valid Luhn number rejected".

Root cause: in checksum() the Luhn doubling is applied to the wrong digit
positions. Counting from the rightmost digit (index 0), Luhn doubles the
digits at odd indices, but checksum() doubles the digits at even indices and
adds the odd-indexed digits without doubling them.

The tests fail on the current code and pass once checksum() doubles the
odd-indexed digits.
"""

import pytest

from alvo import InvalidChecksum, checksum, validate

DIGITS = "0123456789"
HEX = "0123456789abcdef"
ISSUE_NUMBER = "79927398713"


def reference_luhn_valid(number, alphabet=DIGITS):
    """Independent Luhn mod-N check, used to build and sanity-check inputs."""
    n = len(alphabet)
    total = 0
    for index, char in enumerate(reversed(number)):
        value = alphabet.index(char)
        if index % 2 == 1:
            doubled = value * 2
            value = doubled // n + doubled % n
        total += value
    return total % n == 0


def with_check_char(payload, alphabet=DIGITS):
    """Return payload plus the one trailing character that makes it valid."""
    for char in alphabet:
        candidate = payload + char
        if reference_luhn_valid(candidate, alphabet):
            return candidate
    raise AssertionError("no check character makes this payload valid")


def test_reference_agrees_with_issue_example():
    assert reference_luhn_valid(ISSUE_NUMBER)


def test_issue_example_is_accepted():
    assert validate(ISSUE_NUMBER) == ISSUE_NUMBER


def test_checksum_of_issue_example_is_zero():
    assert checksum(ISSUE_NUMBER) == 0


@pytest.mark.parametrize(
    "payload",
    ["1", "12", "123", "7992739871", "4111111111111", "37828224631000"],
)
def test_valid_numbers_are_accepted(payload):
    number = with_check_char(payload)
    assert reference_luhn_valid(number)
    assert checksum(number) == 0
    assert validate(number) == number


@pytest.mark.parametrize("payload", ["1f", "abc", "9"])
def test_valid_numbers_are_accepted_with_hex_alphabet(payload):
    number = with_check_char(payload, HEX)
    assert reference_luhn_valid(number, HEX)
    assert validate(number, HEX) == number


def test_issue_example_with_wrong_check_digit_is_rejected():
    bad = ISSUE_NUMBER[:-1] + "0"
    assert not reference_luhn_valid(bad)
    with pytest.raises(InvalidChecksum):
        validate(bad)


@pytest.mark.parametrize("payload", ["1", "123", "7992739871", "4111111111111"])
def test_wrong_check_digit_is_rejected(payload):
    good = with_check_char(payload)
    wrong_check = "0" if good[-1] != "0" else "1"
    bad = payload + wrong_check
    assert not reference_luhn_valid(bad)
    with pytest.raises(InvalidChecksum):
        validate(bad)
