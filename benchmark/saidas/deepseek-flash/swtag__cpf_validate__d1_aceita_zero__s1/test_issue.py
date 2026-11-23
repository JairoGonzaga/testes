"""Tests reproducing the issue: validate() accepts the all-zeros CPF.

A CPF composed only of zeros (which has valid check digits mathematically,
but is not a real CPF) must be rejected with ``InvalidFormat``.
"""

import pytest

from alvo import InvalidFormat, ValidationError, validate


@pytest.mark.parametrize(
    "number",
    [
        "00000000000",
        "000.000.000-00",
        "000 000 000 00",
        "  00000000000  ",
    ],
)
def test_all_zeros_cpf_is_rejected(number):
    with pytest.raises(InvalidFormat):
        validate(number)


def test_all_zeros_cpf_raises_validation_error():
    with pytest.raises(ValidationError):
        validate("00000000000")


def test_all_zeros_cpf_is_not_accepted_silently():
    # the buggy behaviour: validate() happily returns the number
    try:
        result = validate("00000000000")
    except InvalidFormat:
        return  # expected behaviour
    pytest.fail("validate('00000000000') returned %r instead of raising InvalidFormat" % (result,))


def test_all_zeros_cpf_does_not_raise_checksum_error():
    # the rejection must be a format issue, not a checksum issue
    with pytest.raises(ValidationError) as excinfo:
        validate("00000000000")
    assert not type(excinfo.value).__name__ == "InvalidChecksum", (
        "expected InvalidFormat, got %s" % type(excinfo.value).__name__
    )


@pytest.mark.parametrize(
    "number,expected",
    [
        ("11144477735", "11144477735"),
        ("12345678909", "12345678909"),
        ("111.444.777-35", "11144477735"),
    ],
)
def test_valid_cpf_still_accepted(number, expected):
    assert validate(number) == expected
