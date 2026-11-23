import pytest

from alvo import validate, InvalidFormat, ValidationError


def test_all_zeros_cpf_rejected():
    with pytest.raises(InvalidFormat):
        validate("00000000000")


def test_all_zeros_cpf_rejected_validationerror():
    with pytest.raises(ValidationError):
        validate("00000000000")


@pytest.mark.parametrize("cpf", [
    "00000000000",
    "000.000.000-00",
    " 00000000000 ",
])
def test_all_zeros_variants_rejected(cpf):
    with pytest.raises(InvalidFormat):
        validate(cpf)


def test_valid_cpf_still_accepted():
    from alvo import _calc_check_digits
    base = "111444777"
    cpf = base + _calc_check_digits(base)
    assert validate(cpf) == cpf
