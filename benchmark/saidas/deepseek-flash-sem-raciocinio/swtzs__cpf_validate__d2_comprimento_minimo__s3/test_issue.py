import pytest
from alvo import validate, InvalidLength, InvalidChecksum


def test_cpf_with_too_many_digits_raises_invalid_length():
    with pytest.raises(InvalidLength):
        validate('111444777350')


def test_cpf_with_eleven_digits_wrong_checksum_raises_invalid_checksum():
    with pytest.raises(InvalidChecksum):
        validate('11144477735')


def test_cpf_with_too_few_digits_raises_invalid_length():
    with pytest.raises(InvalidLength):
        validate('1114447773')
