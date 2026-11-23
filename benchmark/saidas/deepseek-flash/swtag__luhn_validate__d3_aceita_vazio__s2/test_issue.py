"""Tests reproducing: validate('') must be rejected with InvalidFormat."""

import pytest

from alvo import (
    InvalidChecksum,
    InvalidFormat,
    ValidationError,
    checksum,
    validate,
)


def test_validate_empty_string_raises_invalid_format():
    """An empty value must be rejected with InvalidFormat, not accepted."""
    with pytest.raises(InvalidFormat):
        validate("")


def test_validate_empty_string_raises_validation_error():
    """The raised exception must be part of the ValidationError hierarchy."""
    with pytest.raises(ValidationError):
        validate("")


def test_validate_empty_string_does_not_raise_invalid_checksum():
    """Empty input is a format problem, not a checksum mismatch."""
    try:
        validate("")
    except InvalidChecksum:
        pytest.fail("validate('') raised InvalidChecksum instead of InvalidFormat")
    except InvalidFormat:
        pass
    else:
        pytest.fail("validate('') was accepted; expected InvalidFormat")


def test_validate_empty_string_with_custom_alphabet():
    """The same rule must hold for any alphabet."""
    with pytest.raises(InvalidFormat):
        validate("", "0246813579")


def test_validate_empty_string_with_long_alphabet():
    """Alphabet of length > 10 must behave the same way."""
    with pytest.raises(InvalidFormat):
        validate("", "0123456789abcdefghijklmnopqrstuvwxyz")


def test_validate_empty_string_returns_nothing():
    """Guard: the buggy return value must not be produced."""
    result = None
    try:
        result = validate("")
    except InvalidFormat:
        return
    pytest.fail("validate('') returned %r instead of raising InvalidFormat" % (result,))


# ---------------------------------------------------------------------------
# Regression tests: non-empty behaviour must be preserved by the fix.
# ---------------------------------------------------------------------------

def test_valid_number_still_accepted():
    number = "1234567812345670"  # valid Luhn number
    assert checksum(number) == 0
    assert validate(number) == number


def test_single_digit_zero_still_accepted():
    assert validate("0") == "0"


def test_wrong_checksum_still_raises_invalid_checksum():
    number = "1234567812345678"  # invalid Luhn checksum
    with pytest.raises(InvalidChecksum):
        validate(number)


def test_non_numeric_still_raises_invalid_format():
    with pytest.raises(InvalidFormat):
        validate("abcdef")


def test_valid_custom_alphabet_number_still_accepted():
    alphabet = "abcdefghij"
    # "aa" has checksum 0 in that alphabet
    assert checksum("aa", alphabet) == 0
    assert validate("aa", alphabet) == "aa"
