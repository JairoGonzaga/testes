"""Tests reproducing the issue: a CPF with too many digits must raise
InvalidLength instead of InvalidChecksum.

See ISSUE.md:

    >>> validate('111444777350')
    alvo.InvalidChecksum   # expected: alvo.InvalidLength
"""

import pytest

from alvo import (
    InvalidChecksum,
    InvalidFormat,
    InvalidLength,
    compact,
    validate,
)


def test_issue_example_raises_invalid_length():
    """The exact example from the issue report."""
    with pytest.raises(InvalidLength):
        validate("111444777350")


def test_too_long_number_raises_invalid_length_not_checksum():
    """A too long CPF must raise InvalidLength (and not InvalidChecksum)."""
    with pytest.raises(InvalidLength) as excinfo:
        validate("111444777350")
    assert not isinstance(excinfo.value, InvalidChecksum)


@pytest.mark.parametrize(
    "number",
    [
        "111444777350",       # 12 digits
        "1114447773500",      # 13 digits
        "11144477735000",     # 14 digits
        "011144477735",       # 12 digits, leading zero
        "11144477735" + "9",  # 12 digits, bad verifier digit too
    ],
)
def test_numbers_with_more_than_eleven_digits(number):
    assert len(compact(number)) != 11
    with pytest.raises(InvalidLength):
        validate(number)


def test_formatted_too_long_number_raises_invalid_length():
    """The length check must be done on the compacted number."""
    with pytest.raises(InvalidLength):
        validate("111.444.777-350")


@pytest.mark.parametrize(
    "number",
    [
        "1",
        "1114447773",       # 10 digits
        "1.114.447.7",      # formatted, too short
    ],
)
def test_numbers_with_fewer_than_eleven_digits_still_invalid_length(number):
    with pytest.raises(InvalidLength):
        validate(number)


def test_invalid_length_is_a_validation_error():
    with pytest.raises(InvalidLength) as excinfo:
        validate("111444777350")
    assert isinstance(excinfo.value, (InvalidFormat, ValueError))


@pytest.mark.parametrize(
    ("number", "expected"),
    [
        ("11144477735", "11144477735"),
        ("111.444.777-35", "11144477735"),
        ("111 444 777 35", "11144477735"),
        (" 11144477735 ", "11144477735"),
    ],
)
def test_valid_cpf_is_still_accepted(number, expected):
    """Regression guard: a well formed 11 digit CPF must still validate."""
    assert validate(number) == expected
