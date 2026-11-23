import pytest

from alvo import validate, compact, InvalidFormat


def test_compact_removes_dots_and_hyphens():
    assert compact("111.444.777-35") == "11144477735"


def test_validate_accepts_formatted_cpf():
    assert validate("111.444.777-35") == "11144477735"


def test_validate_accepts_formatted_cpf_with_spaces():
    assert validate(" 111.444.777-35 ") == "11144477735"


def test_validate_still_rejects_non_digits():
    with pytest.raises(InvalidFormat):
        validate("111.444.777-3X")
