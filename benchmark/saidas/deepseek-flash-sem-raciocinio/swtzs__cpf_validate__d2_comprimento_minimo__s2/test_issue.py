import pytest

from alvo import validate, InvalidLength, InvalidChecksum, InvalidFormat


def test_cpf_with_twelve_digits_raises_invalid_length():
    with pytest.raises(InvalidLength):
        validate('111444777350')


def test_cpf_with_too_many_digits_formatted_raises_invalid_length():
    with pytest.raises(InvalidLength):
        validate('111.444.777-350')
