from alvo import validate


def test_validate_accepts_formatted_cpf_with_dots():
    assert validate("111.444.777-35") == "11144477735"


def test_validate_accepts_formatted_cpf_with_dots_and_surrounding_spaces():
    assert validate(" 111.444.777-35 ") == "11144477735"
