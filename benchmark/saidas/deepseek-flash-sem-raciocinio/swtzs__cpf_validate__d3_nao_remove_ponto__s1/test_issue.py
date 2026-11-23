import pytest

from alvo import validate, InvalidFormat


def test_validate_dotted_cpf_returns_compact():
    assert validate('111.444.777-35') == '11144477735'


def test_validate_dotted_cpf_does_not_raise_invalid_format():
    try:
        validate('111.444.777-35')
    except InvalidFormat:
        pytest.fail("validate() rejected a correctly formatted CPF with dots")


def test_validate_dotted_cpf_equals_plain_cpf():
    assert validate('111.444.777-35') == validate('11144477735')
