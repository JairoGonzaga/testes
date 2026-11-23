"""Reproduction tests for the issue: validate('') accepts an empty string.

An empty value must be rejected with InvalidFormat instead of being
silently accepted (checksum('') == 0 makes it look "valid").
"""

import pytest

from alvo import (
    InvalidChecksum,
    InvalidFormat,
    ValidationError,
    checksum,
    validate,
)


def test_empty_string_is_rejected():
    """The core bug: validate('') must raise InvalidFormat."""
    with pytest.raises(InvalidFormat):
        validate('')


def test_empty_string_is_rejected_not_just_checksum_error():
    """The empty value is a *format* problem, not a checksum mismatch."""
    with pytest.raises(InvalidFormat) as excinfo:
        validate('')
    assert isinstance(excinfo.value, ValidationError)
    assert not isinstance(excinfo.value, InvalidChecksum)


def test_empty_value_rejected_with_custom_alphabet():
    """An empty value must be rejected regardless of the alphabet used."""
    alphabet = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    with pytest.raises(InvalidFormat):
        validate('', alphabet)


def test_empty_value_rejected_for_non_default_alphabet_hex():
    with pytest.raises(InvalidFormat):
        validate('', "0123456789abcdef")


@pytest.mark.parametrize("value", ['', ])
def test_empty_string_never_returned(value):
    """validate() must never return an empty value back to the caller."""
    try:
        result = validate(value)
    except InvalidFormat:
        return
    pytest.fail("validate(%r) returned %r instead of raising InvalidFormat"
                % (value, result))


# --- regression guards: behaviour that must keep working after the fix ---


def test_valid_numbers_are_still_accepted():
    for value in ('79927398713', '4111111111111111', '1234567812345670', '0'):
        assert validate(value) == value


def test_invalid_checksum_still_raises_invalid_checksum():
    with pytest.raises(InvalidChecksum):
        validate('79927398714')


def test_non_empty_invalid_format_still_raises_invalid_format():
    with pytest.raises(InvalidFormat):
        validate('12a4')


def test_checksum_of_empty_string_is_zero():
    """Documenting why the bug happens (checksum alone cannot reject '')."""
    assert checksum('') == 0
