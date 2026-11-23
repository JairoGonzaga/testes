"""Reproduction tests for ISSUE.md.

Any CPF whose compacted form does not have exactly 11 digits must raise
``InvalidLength``.  The current implementation only guards against *short*
numbers (``len(number) < 11``), so numbers longer than 11 digits fall through
to the checksum verification and raise ``InvalidChecksum`` -- or, when the last
two digits happen to match the check digits of the first nine, are even
returned as valid.
"""

import pytest

from alvo import (
    InvalidChecksum,
    InvalidLength,
    compact,
    validate,
)

# 12 digits, trailing digits do not match the check digits of the first 9
# -> currently raises InvalidChecksum (the example from the issue report).
TOO_LONG_BAD_CHECKSUM = "111444777350"

# 12 digits whose last two digits *do* match the check digits of the first 9
# -> currently accepted as valid instead of being rejected for its length.
TOO_LONG_GOOD_CHECKSUM = "111444777035"

# A genuinely valid CPF, used as a regression guard.
VALID_CPF = "11144477735"


def test_issue_example_raises_invalid_length():
    """The exact example from the issue report."""
    with pytest.raises(InvalidLength):
        validate("111444777350")


@pytest.mark.parametrize(
    "number",
    [
        TOO_LONG_BAD_CHECKSUM,      # 12 digits, bad check digits
        TOO_LONG_GOOD_CHECKSUM,     # 12 digits, coincidentally good check digits
        "1114447773509",            # 13 digits
        "11144477735098765",        # 17 digits
        "111.444.777-350",          # 12 digits once compacted (formatted)
        " 111444777350 ",           # 12 digits once compacted (padded)
        "1114447773500000",         # 16 digits
    ],
)
def test_too_many_digits_raises_invalid_length(number):
    """Any number with more than 11 compacted digits must raise InvalidLength."""
    assert len(compact(number)) > 11  # sanity check on the fixture itself
    with pytest.raises(InvalidLength):
        validate(number)


@pytest.mark.parametrize(
    "number",
    [
        "1114447773",               # 10 digits
        "111444777",                # 9 digits
        "1",                        # 1 digit
        "111.444.777-3",            # 10 digits once compacted
        "1114447773 ",              # 10 digits once compacted, padded
    ],
)
def test_too_few_digits_raises_invalid_length(number):
    """Short numbers already raise InvalidLength and must keep doing so."""
    assert len(compact(number)) < 11  # sanity check on the fixture itself
    with pytest.raises(InvalidLength):
        validate(number)


@pytest.mark.parametrize("number", [TOO_LONG_BAD_CHECKSUM, TOO_LONG_GOOD_CHECKSUM])
def test_length_error_is_not_reported_as_checksum_error(number):
    """A wrong length must never surface as InvalidChecksum (or as success)."""
    try:
        validate(number)
    except InvalidLength:
        pass
    except InvalidChecksum:
        pytest.fail(
            "validate(%r) raised InvalidChecksum; a number with the wrong "
            "length must raise InvalidLength" % (number,)
        )
    else:
        pytest.fail(
            "validate(%r) returned without error; a number with the wrong "
            "length must raise InvalidLength" % (number,)
        )


def test_valid_cpf_still_validated():
    """A correct 11-digit CPF must still be accepted."""
    assert validate(VALID_CPF) == VALID_CPF
    assert validate("111.444.777-35") == VALID_CPF


def test_valid_length_with_wrong_checksum_raises_invalid_checksum():
    """Checksum errors for 11-digit numbers must not become length errors."""
    with pytest.raises(InvalidChecksum):
        validate("11144477736")
