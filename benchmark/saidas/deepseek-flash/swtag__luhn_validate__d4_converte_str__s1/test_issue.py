"""Tests reproducing the issue: validate() must return the value it received unchanged."""

import pytest

from alvo import InvalidChecksum, InvalidFormat, checksum, validate

# Classic Luhn-valid number (see https://en.wikipedia.org/wiki/Luhn_algorithm).
VALID_NUMBER = 79927398713


def test_checksum_of_valid_number_is_zero():
    assert checksum(VALID_NUMBER) == 0


def test_validate_returns_int_unchanged_when_given_int():
    """validate(79927398713) must return the int, not its string representation."""
    result = validate(VALID_NUMBER)
    assert result == VALID_NUMBER
    assert isinstance(result, int)
    assert not isinstance(result, str)


def test_validate_keeps_result_type_for_int():
    result = validate(VALID_NUMBER)
    assert type(result) is type(VALID_NUMBER)
    assert repr(result) == repr(VALID_NUMBER)


def test_validate_returns_str_unchanged_when_given_str():
    text = str(VALID_NUMBER)
    result = validate(text)
    assert result == text
    assert isinstance(result, str)


def test_validate_returns_same_object_for_int():
    """The very value passed in should come back (identity for ints)."""
    assert validate(VALID_NUMBER) is VALID_NUMBER


def test_validate_valid_int_does_not_raise():
    # Should simply succeed, no matter which value type is returned.
    validate(VALID_NUMBER)


@pytest.mark.parametrize("bad", [79927398710, 79927398711, 79927398712, 79927398714])
def test_validate_still_rejects_invalid_int(bad):
    with pytest.raises(InvalidChecksum):
        validate(bad)


def test_validate_still_rejects_empty_input():
    with pytest.raises(InvalidFormat):
        validate("")


def test_validate_still_rejects_non_numeric_input():
    with pytest.raises(InvalidFormat):
        validate("not-a-number")
