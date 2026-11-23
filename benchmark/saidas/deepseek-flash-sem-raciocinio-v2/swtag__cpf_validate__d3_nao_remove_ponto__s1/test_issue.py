import pytest

from alvo import validate


def test_validate_formatted_cpf_with_dots():
    assert validate('111.444.777-35') == '11144477735'


def test_validate_plain_cpf():
    assert validate('11144477735') == '11144477735'
