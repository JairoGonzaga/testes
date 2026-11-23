import pytest

from alvo import validate, InvalidChecksum


def test_validate_known_valid_cpf_digits_only():
    assert validate("11144477735") == "11144477735"


def test_validate_known_valid_cpf_formatted():
    assert validate("111.444.777-35") == "11144477735"


def test_validate_other_known_valid_cpf():
    assert validate("529.982.247-25") == "52998224725"
