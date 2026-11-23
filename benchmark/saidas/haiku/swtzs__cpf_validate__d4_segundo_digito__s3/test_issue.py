import pytest

from alvo import validate


@pytest.mark.parametrize(
    "cpf",
    [
        "11144477735",
        "52998224725",
    ],
)
def test_valid_cpf_is_accepted(cpf):
    assert validate(cpf) == cpf


def test_issue_example_111_444_777_35():
    assert validate("11144477735") == "11144477735"


def test_formatted_valid_cpf_is_accepted():
    assert validate("111.444.777-35") == "11144477735"
