import pytest

from alvo import validate, compact, InvalidFormat, InvalidLength, InvalidChecksum


def test_validate_formatted_cpf_with_dots():
    assert validate("111.444.777-35") == "11144477735"


def test_compact_removes_dots_spaces_and_hyphens():
    assert compact("111.444.777-35") == "11144477735"
    assert compact(" 111.444.777-35 ") == "11144477735"


def test_validate_formatted_cpf_with_spaces():
    assert validate("111 444 777 35") == "11144477735"


def test_validate_unformatted_cpf():
    assert validate("11144477735") == "11144477735"


def test_validate_another_formatted_cpf():
    # 529.982.247-25 is a well-known valid CPF
    assert validate("529.982.247-25") == "52998224725"


def test_validate_invalid_checksum_formatted():
    with pytest.raises(InvalidChecksum):
        validate("111.444.777-36")


def test_validate_invalid_length_formatted():
    with pytest.raises(InvalidLength):
        validate("111.444.777-3")


def test_validate_letters_rejected():
    with pytest.raises(InvalidFormat):
        validate("111.444.777-3a")
