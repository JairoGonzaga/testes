"""Reproduction tests for the issue described in ISSUE.md.

`validate()` must return the value it received, unchanged, when the value is
valid.  Currently it always converts the value with ``str()``, so passing an
``int`` returns a ``str``.
"""

import pytest

from alvo import validate

VALID_INTS = [
    79927398713,        # example from the issue
    4111111111111111,
    4012888888881881,
    12345674,
]


@pytest.mark.parametrize("number", VALID_INTS)
def test_validate_returns_the_int_it_received(number):
    result = validate(number)
    assert not isinstance(result, str), (
        "validate() returned %r instead of the int %r" % (result, number)
    )
    assert isinstance(result, int)
    assert result == number


@pytest.mark.parametrize("number", VALID_INTS)
def test_validate_preserves_input_type_for_int(number):
    assert type(validate(number)) is type(number)


def test_validate_returns_value_unchanged_for_ints_and_strs():
    """The return value equals the input *and* keeps the input's type."""
    values = list(VALID_INTS) + [str(number) for number in VALID_INTS]
    for value in values:
        result = validate(value)
        assert result == value, "validate(%r) returned %r" % (value, result)
        assert type(result) is type(value), (
            "validate(%r) returned a %s instead of a %s"
            % (value, type(result).__name__, type(value).__name__)
        )


def test_validate_int_can_be_used_as_an_int():
    """A typical caller using the result as a number must not break."""
    result = validate(79927398713)
    assert result + 1 == 79927398714
