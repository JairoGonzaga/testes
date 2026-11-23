"""Tests reproducing the issue: ``validate()`` accepts the all-zeros CPF.

A CPF composed only of zeros (``00000000000``) is not a valid number and must
be rejected with ``InvalidFormat`` instead of being returned unchanged.
"""

import pytest

from alvo import InvalidChecksum, InvalidFormat, InvalidLength, validate


def test_all_zeros_is_rejected():
    """The all-zeros CPF must raise InvalidFormat (issue)."""
    with pytest.raises(InvalidFormat):
        validate("00000000000")


def test_all_zeros_error_is_not_a_checksum_error():
    """The all-zeros CPF is a format problem, not a checksum problem."""
    with pytest.raises(InvalidFormat) as excinfo:
        validate("00000000000")
    assert not isinstance(excinfo.value, InvalidChecksum)


def test_all_zeros_with_mask_is_rejected():
    """The masked all-zeros CPF must be rejected as well."""
    with pytest.raises(InvalidFormat):
        validate("000.000.000-00")


def test_all_zeros_with_whitespace_is_rejected():
    """The all-zeros CPF surrounded by whitespace must be rejected as well."""
    with pytest.raises(InvalidFormat):
        validate("  00000000000  ")


def test_valid_cpf_is_still_accepted():
    """A genuinely valid CPF must keep being accepted."""
    assert validate("52998224725") == "52998224725"


def test_valid_cpf_with_mask_is_still_accepted():
    """A genuinely valid, masked CPF must keep being accepted."""
    assert validate("529.982.247-25") == "52998224725"


def test_invalid_checksum_is_still_rejected():
    """A CPF with a wrong check digit must still raise InvalidChecksum."""
    with pytest.raises(InvalidChecksum):
        validate("52998224724")


def test_wrong_length_is_still_rejected():
    """A too short CPF must still raise InvalidLength."""
    with pytest.raises(InvalidLength):
        validate("1234567890")


def test_non_digits_are_still_rejected():
    """Non-digit characters must still raise InvalidFormat."""
    with pytest.raises(InvalidFormat):
        validate("abcdefghijk")
