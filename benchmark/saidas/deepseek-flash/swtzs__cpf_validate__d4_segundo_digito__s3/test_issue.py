from alvo import validate


def test_known_valid_cpf_is_accepted():
    assert validate("11144477735") == "11144477735"


def test_known_valid_formatted_cpf_is_accepted_and_compacted():
    assert validate("111.444.777-35") == "11144477735"
