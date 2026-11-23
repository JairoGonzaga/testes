import pytest

from alvo import InvalidFormat, validate


@pytest.mark.parametrize("cpf", [
    "00000000000",
    "000.000.000-00",
])
def test_all_zeros_cpf_is_rejected(cpf):
    with pytest.raises(InvalidFormat):
        validate(cpf)


def test_valid_cpf_is_still_accepted():
    assert validate("529.982.247-25") == "52998224725"
