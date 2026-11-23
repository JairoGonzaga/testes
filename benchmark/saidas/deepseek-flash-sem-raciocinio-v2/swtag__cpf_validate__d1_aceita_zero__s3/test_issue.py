import pytest

from alvo import validate, InvalidFormat
from alvo import _calc_check_digits


def _valid_cpf(base9):
    return base9 + _calc_check_digits(base9)


def test_all_zeros_cpf_is_rejected():
    with pytest.raises(InvalidFormat):
        validate("00000000000")


def test_all_zeros_cpf_with_formatting_is_rejected():
    with pytest.raises(InvalidFormat):
        validate("000.000.000-00")


def test_all_zeros_cpf_is_rejected_even_with_correct_check_digits():
    # check digits computed by the module itself, so InvalidChecksum is not the issue
    number = _valid_cpf("000000000")
    with pytest.raises(InvalidFormat):
        validate(number)


def test_valid_cpf_still_accepted():
    number = _valid_cpf("529982247")
    assert validate(number) == number
