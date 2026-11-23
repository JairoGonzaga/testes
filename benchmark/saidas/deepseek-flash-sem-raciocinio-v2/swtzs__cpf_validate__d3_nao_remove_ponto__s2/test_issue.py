from alvo import validate


def test_validate_formatted_cpf_with_dots():
    assert validate('111.444.777-35') == '11144477735'
