"""Reproduces: CPFs with more than 11 digits raise InvalidChecksum instead of
InvalidLength (see ISSUE.md)."""

import pytest

from alvo import InvalidChecksum, InvalidFormat, InvalidLength, compact, validate

VALID = "11144477735"

# All-digit strings whose compacted form has more than 11 digits.
TOO_LONG = [
    "111444777350",  # 12 digits (the case from the issue)
    "1114447773500",  # 13 digits
    "111444777350000",  # 15 digits
    "1" * 12,
    "0" * 11 + "1",
]


def test_too_long_reported_in_issue():
    # Exact snippet from ISSUE.md
    with pytest.raises(InvalidLength):
        validate("111444777350")


@pytest.mark.parametrize("number", TOO_LONG)
def test_more_than_11_digits_raises_invalid_length(number):
    assert len(compact(number)) > 11
    with pytest.raises(InvalidLength):
        validate(number)


@pytest.mark.parametrize("number", TOO_LONG)
def test_more_than_11_digits_is_not_invalid_checksum(number):
    # InvalidLength is a subclass of InvalidFormat but NOT of InvalidChecksum,
    # so this also guards against the wrong exception type being raised.
    with pytest.raises(InvalidFormat) as excinfo:
        validate(number)
    assert isinstance(excinfo.value, InvalidLength)
    assert not isinstance(excinfo.value, InvalidChecksum)


def test_too_short_still_raises_invalid_length():
    with pytest.raises(InvalidLength):
        validate("1114447773")


def test_valid_cpf_is_returned_compacted():
    assert validate("111.444.777-35") == VALID
    assert validate(VALID) == VALID


def test_non_digits_still_raise_invalid_format():
    with pytest.raises(InvalidFormat):
        validate("1114447773a")
