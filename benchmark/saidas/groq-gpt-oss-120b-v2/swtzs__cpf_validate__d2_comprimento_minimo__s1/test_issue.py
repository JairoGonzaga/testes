import pytest
from alvo import validate, InvalidLength

def test_cpf_with_too_many_digits_raises_invalid_length():
    """
    A CPF longer than 11 digits must raise InvalidLength.
    The current buggy implementation raises InvalidChecksum,
    so this test fails until the bug is fixed.
    """
    with pytest.raises(InvalidLength):
        validate('111444777350')
