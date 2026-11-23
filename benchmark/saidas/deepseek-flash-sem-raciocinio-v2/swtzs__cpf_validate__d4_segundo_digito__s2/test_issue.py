import pytest

from alvo import validate, InvalidChecksum


def test_known_valid_cpf_returns_compact_number():
    assert validate('11144477735') == '11144477735'


def test_known_valid_cpf_formatted_returns_compact_number():
    assert validate('111.444.777-35') == '11144477735'


def test_known_valid_cpf_does_not_raise_invalid_checksum():
    try:
        result = validate('11144477735')
    except InvalidChecksum:
        pytest.fail("validate raised InvalidChecksum for a valid CPF")
    assert result == '11144477735'
