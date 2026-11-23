import pytest

from alvo import validate, InvalidLength


def test_cpf_with_12_digits_raises_invalid_length():
    # From the issue: too many digits should be InvalidLength, not InvalidChecksum.
    with pytest.raises(InvalidLength):
        validate("111444777350")


def test_cpf_with_13_digits_raises_invalid_length():
    # Any compacted form not exactly 11 digits should be InvalidLength.
    with pytest.raises(InvalidLength):
        validate("1114447773501")
