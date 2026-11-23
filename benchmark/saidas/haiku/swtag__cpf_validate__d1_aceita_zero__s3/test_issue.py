import pytest

from alvo import InvalidFormat, validate


def test_all_zeros_cpf_is_rejected():
    with pytest.raises(InvalidFormat):
        validate('00000000000')


@pytest.mark.parametrize('number', ['000.000.000-00', '000 000 000 00'])
def test_all_zeros_cpf_with_formatting_is_rejected(number):
    with pytest.raises(InvalidFormat):
        validate(number)


def test_valid_cpf_is_still_accepted():
    assert validate('11144477735') == '11144477735'
