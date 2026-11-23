import pytest

from alvo import InvalidFormat, validate


def test_all_zeros_cpf_is_rejected():
    with pytest.raises(InvalidFormat):
        validate('00000000000')


def test_all_zeros_masked_cpf_is_rejected():
    with pytest.raises(InvalidFormat):
        validate('000.000.000-00')


def test_valid_cpf_is_still_accepted():
    assert validate('529.982.247-25') == '52998224725'
