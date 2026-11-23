"""Regression tests for the issue: validate('') accepts an empty string.

An empty value must be rejected with InvalidFormat instead of being
silently accepted (checksum('') happens to be 0, hence "valid").
"""

import pytest

from alvo import InvalidChecksum, InvalidFormat, ValidationError, checksum, validate


# ---------------------------------------------------------------------------
# Core reproduction of the issue
# ---------------------------------------------------------------------------

def test_validate_empty_string_raises_invalid_format():
    """validate('') must raise InvalidFormat (currently returns '')."""
    with pytest.raises(InvalidFormat):
        validate("")


def test_validate_empty_string_does_not_return_value():
    """The empty string must not be accepted as a valid value."""
    returned = object()
    try:
        returned = validate("")
    except ValidationError:
        return  # any validation error is fine here; the bug is returning
    pytest.fail(f"validate('') returned {returned!r} instead of raising")


def test_validate_empty_string_raises_format_error_not_checksum_error():
    """A missing value is a format problem, not a checksum problem."""
    with pytest.raises(InvalidFormat) as excinfo:
        validate("")
    assert not isinstance(excinfo.value, InvalidChecksum)


def test_empty_string_is_reported_as_validation_error():
    """InvalidFormat raised for '' is a ValidationError (catchable broadly)."""
    with pytest.raises(ValidationError):
        validate("")


def test_validate_empty_string_with_custom_alphabet():
    """The empty value must be rejected for any alphabet, not just digits."""
    with pytest.raises(InvalidFormat):
        validate("", "0123456789abcdefghijklmnopqrstuvwxyz")


def test_validate_empty_string_positional_and_keyword():
    with pytest.raises(InvalidFormat):
        validate("", "0123456789")
    with pytest.raises(InvalidFormat):
        validate("", alphabet="0123456789")


# ---------------------------------------------------------------------------
# Guard rails: behaviour that must not regress
# ---------------------------------------------------------------------------

@pytest.mark.parametrize(
    "number",
    [
        "0",
        "18",
        "1230",
        "79927398713",
        "4111111111111111",
    ],
)
def test_valid_numbers_are_still_accepted(number):
    assert validate(number) == number
    assert checksum(number) == 0


@pytest.mark.parametrize("number", ["1", "19", "1231", "4111111111111112"])
def test_invalid_numbers_still_raise_invalid_checksum(number):
    with pytest.raises(InvalidChecksum):
        validate(number)


def test_non_numeric_input_still_raises_invalid_format():
    with pytest.raises(InvalidFormat):
        validate("not-a-number")
