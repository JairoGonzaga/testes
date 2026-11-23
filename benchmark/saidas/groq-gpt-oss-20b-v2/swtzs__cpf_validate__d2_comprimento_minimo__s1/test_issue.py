import pytest
from alvo import validate, InvalidLength


def test_invalid_length_long():
    """CPF with more than 11 digits should raise InvalidLength (currently raises InvalidChecksum)."""
    with pytest.raises(InvalidLength):
        validate("111444777350")
