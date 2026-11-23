import pytest

from alvo import validate


def test_valid_cpf_11144477735():
    assert validate('11144477735') == '11144477735'


def test_valid_cpf_formatted():
    assert validate('111.444.777-35') == '11144477735'
