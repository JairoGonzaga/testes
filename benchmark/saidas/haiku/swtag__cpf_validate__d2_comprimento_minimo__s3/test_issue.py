import pytest

from alvo import InvalidLength, validate


def test_twelve_digits_raises_invalid_length():
    # Issue example: 12 digits must be reported as a length error,
    # not as a checksum error.
    with pytest.raises(InvalidLength):
        validate("111444777350")


def test_twelve_digits_with_matching_check_digits_raises_invalid_length():
    # The last two digits match the check digits computed from the first
    # nine, so the current code accepts this over-long number silently.
    with pytest.raises(InvalidLength):
        validate("111444777035")


def test_thirteen_digits_raises_invalid_length():
    with pytest.raises(InvalidLength):
        validate("1114447773500")


def test_formatted_twelve_digits_raises_invalid_length():
    # Punctuation is stripped before the length is checked.
    with pytest.raises(InvalidLength):
        validate("111.444.777-350")


def test_valid_cpf_still_accepted():
    assert validate("111.444.777-35") == "11144477735"


def test_too_short_still_raises_invalid_length():
    with pytest.raises(InvalidLength):
        validate("1114447773")
