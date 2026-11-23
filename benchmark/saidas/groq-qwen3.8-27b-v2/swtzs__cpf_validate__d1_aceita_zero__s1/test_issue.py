import pytest

from alvo import InvalidFormat, validate


def test_all_zeros_cpf_rejected():
    # The issue states validate('00000000000') currently returns
    # '00000000000' but the all-zeros CPF should be rejected with InvalidFormat.
    with pytest.raises(InvalidFormat):
        validate("00000000000")
