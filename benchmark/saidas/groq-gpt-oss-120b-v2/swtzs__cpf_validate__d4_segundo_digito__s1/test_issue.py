import pytest
from alvo import validate, InvalidChecksum


def test_valid_cpf_is_accepted():
    """A known valid CPF should be accepted and returned unchanged."""
    assert validate('11144477735') == '11144477735'
