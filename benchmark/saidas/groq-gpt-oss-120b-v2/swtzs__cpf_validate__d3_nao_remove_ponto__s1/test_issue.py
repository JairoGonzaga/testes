import pytest
from alvo import validate, InvalidFormat


def test_validate_formatted_cpf_returns_compact():
    """
    A CPF in the usual dotted format must be accepted and returned in its
    compact numeric form. The current implementation incorrectly raises
    InvalidFormat because dots are not stripped.
    """
    # This should succeed and return the compact representation.
    result = validate("111.444.777-35")
    assert result == "11144477735"
