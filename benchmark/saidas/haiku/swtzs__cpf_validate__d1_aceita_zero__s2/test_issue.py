import pytest

from alvo import InvalidFormat, validate


@pytest.mark.parametrize("cpf", ["00000000000", "000.000.000-00"])
def test_all_zeros_cpf_is_rejected(cpf):
    with pytest.raises(InvalidFormat):
        validate(cpf)
