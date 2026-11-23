import pytest

from alvo import validate


def test_issue_example_valid_cpf_is_accepted():
    assert validate('11144477735') == '11144477735'


def test_formatted_valid_cpf_is_accepted():
    assert validate('111.444.777-35') == '11144477735'


@pytest.mark.parametrize("cpf", ['52998224725', '11144477735'])
def test_valid_cpf_returns_normalized_digits(cpf):
    assert validate(cpf) == cpf
