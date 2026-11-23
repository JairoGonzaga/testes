import pytest
from alvo import validate, InvalidFormat

def test_all_zeros_cpf_is_invalid():
    """All‑zeros CPF must be rejected with InvalidFormat."""
    with pytest.raises(InvalidFormat):
        validate('00000000000')
