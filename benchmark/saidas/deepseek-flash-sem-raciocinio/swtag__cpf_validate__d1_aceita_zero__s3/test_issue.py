import pytest

from alvo import InvalidFormat, validate


def test_all_zeros_cpf_rejected():
    with pytest.raises(InvalidFormat):
        validate("00000000000")


def test_all_zeros_cpf_rejected_with_formatting():
    with pytest.raises(InvalidFormat):
        validate("000.000.000-00")


def test_all_repeated_digits_rejected():
    for d in "0123456789":
        with pytest.raises(InvalidFormat):
            validate(d * 11)


def test_valid_cpf_still_accepted():
    assert validate("529.982.247-25") == "52998224725"
