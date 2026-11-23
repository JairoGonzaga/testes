"""Tests reproducing the issue: formatted CPFs (with dots) are rejected.

See ISSUE.md: ``validate()`` must accept CPFs in the usual ``XXX.XXX.XXX-XX``
format, stripping spaces, dots and hyphens before validation, and return the
compact form.
"""

import pytest

from alvo import InvalidChecksum, InvalidFormat, InvalidLength, compact, validate


def test_validate_accepts_cpf_with_dots_and_hyphen():
    assert validate("111.444.777-35") == "11144477735"


def test_validate_accepts_cpf_with_only_dots():
    assert validate("111.444.77735") == "11144477735"


def test_validate_accepts_cpf_with_spaces():
    assert validate(" 111 444 777 35 ") == "11144477735"


def test_validate_accepts_mixed_formatting():
    assert validate("111.444.777 35") == "11144477735"


def test_compact_removes_dots_hyphens_and_spaces():
    assert compact("111.444.777-35") == "11144477735"
    assert compact(" 111.444.777-35 ") == "11144477735"


def test_validate_formatted_invalid_checksum_raises_checksum_error():
    # A formatted number with a wrong check digit must fail on the checksum,
    # not on the format (i.e. the dots must have been stripped).
    with pytest.raises(InvalidChecksum):
        validate("111.444.777-36")


def test_validate_formatted_invalid_length_raises_length_error():
    with pytest.raises(InvalidLength):
        validate("111.444.777-3")


def test_validate_plain_digits_still_works():
    assert validate("11144477735") == "11144477735"


def test_validate_unformatted_invalid_checksum_still_raises():
    with pytest.raises(InvalidChecksum):
        validate("11144477736")


def test_validate_non_digit_chars_still_raise_invalid_format():
    with pytest.raises(InvalidFormat):
        validate("111.444.777-3a")
