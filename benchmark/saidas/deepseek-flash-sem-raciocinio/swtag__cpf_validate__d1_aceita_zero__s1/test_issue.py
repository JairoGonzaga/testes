import pytest

from alvo import validate, InvalidFormat, InvalidChecksum


def test_all_zeros_is_rejected():
    with pytest.raises(InvalidFormat):
        validate("00000000000")


def test_all_zeros_with_formatting_is_rejected():
    with pytest.raises(InvalidFormat):
        validate("000.000.000-00")


def test_other_repeated_digits_are_rejected():
    for digit in "123456789":
        with pytest.raises(InvalidFormat):
            validate(digit * 11)


def test_valid_cpf_still_accepted():
    assert validate("529.982.247-25") == "52998224725"


def test_invalid_checksum_still_rejected():
    with pytest.raises(InvalidChecksum):
        validate("52998224724")
