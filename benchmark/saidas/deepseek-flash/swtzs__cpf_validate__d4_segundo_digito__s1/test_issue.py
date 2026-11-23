import pytest

from alvo import validate, InvalidChecksum


def test_valid_cpf_11144477735_is_accepted():
    assert validate("11144477735") == "11144477735"


def test_valid_formatted_cpf_is_accepted():
    assert validate("111.444.777-35") == "11144477735"


def test_invalid_cpf_is_still_rejected():
    with pytest.raises(InvalidChecksum):
        validate("11144477736")
