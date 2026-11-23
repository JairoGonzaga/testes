import pytest

from alvo import InvalidLength, validate


def test_cpf_with_12_digits_raises_invalid_length():
    with pytest.raises(InvalidLength):
        validate('111444777350')
