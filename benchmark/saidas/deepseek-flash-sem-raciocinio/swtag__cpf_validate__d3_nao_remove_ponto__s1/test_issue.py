import pytest

from alvo import validate, compact


def test_validate_formatted_cpf_with_dots():
    assert validate("111.444.777-35") == "11144477735"


def test_validate_formatted_plain_cpf():
    assert validate("11144477735") == "11144477735"


def test_validate_formatted_with_spaces():
    assert validate(" 111.444.777-35 ") == "11144477735"


def test_compact_removes_dots():
    assert compact("111.444.777-35") == "11144477735"
