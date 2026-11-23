import pytest

from alvo import validate, InvalidChecksum


def test_known_valid_cpf_with_correct_check_digits():
    assert validate('11144477735') == '11144477735'


def test_known_valid_formatted_cpf():
    assert validate('111.444.777-35') == '11144477735'


def test_invalid_checksum_still_rejected():
    with pytest.raises(InvalidChecksum):
        validate('11144477736')
