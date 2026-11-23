"""Reproduction tests for ISSUE.md:

``validate()`` must return the value it received unchanged when it is valid.
Currently it always does ``return str(number)``, so passing an ``int`` comes
back as a ``str``.
"""

import pytest

from alvo import validate


VALID_INT = 79927398713          # Luhn-valid
VALID_INT_STR = "79927398713"    # same number, as a string
VALID_VISA = 4539578763621486    # another Luhn-valid int
INVALID_INT = 79927398714


def test_validate_returns_the_int_unchanged():
    """validate(79927398713) must return the int 79927398713, not '79927398713'."""
    result = validate(VALID_INT)

    assert result == VALID_INT
    assert not isinstance(result, str), (
        "validate() converted the int %r into the string %r" % (VALID_INT, result)
    )
    assert isinstance(result, int)
    assert type(result) is int


def test_validate_preserves_the_type_of_the_input():
    """Whatever type goes in must come out (unchanged value, unchanged type)."""
    for value in (VALID_INT, VALID_VISA):
        result = validate(value)
        assert type(result) is type(value)
        assert result == value


def test_validate_does_not_stringify_the_input():
    """The returned object must be the very object that was passed in."""
    sentinel = VALID_INT
    result = validate(sentinel)

    assert result is sentinel


def test_validate_returns_the_string_unchanged():
    """A valid string input keeps being returned as the same string."""
    result = validate(VALID_INT_STR)

    assert result == VALID_INT_STR
    assert type(result) is str
    assert result is VALID_INT_STR


@pytest.mark.parametrize("value", [VALID_INT, VALID_INT_STR, VALID_VISA])
def test_valid_inputs_are_not_rejected_or_rewritten(value):
    """Sanity check: validating a valid number neither raises nor mangles it."""
    result = validate(value)
    assert result == value
    assert str(result) == str(value)
    assert type(result) is type(value)


def test_invalid_int_still_raises():
    """Sanity check: the error behaviour for a bad checksum is unchanged."""
    from alvo import InvalidChecksum

    with pytest.raises(InvalidChecksum):
        validate(INVALID_INT)
