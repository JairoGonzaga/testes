from alvo import validate


def test_cpf_with_dots_and_hyphen_is_accepted():
    # Issue: 'XXX.XXX.XXX-XX' must be accepted; dots, spaces and hyphens are removed before validating.
    assert validate('111.444.777-35') == '11144477735'


def test_cpf_with_dots_and_hyphen_returns_compact_form_other_value():
    assert validate('529.982.247-25') == '52998224725'


def test_cpf_with_dots_only_is_accepted():
    assert validate('111.444.77735') == '11144477735'


def test_cpf_with_dots_and_spaces_is_accepted():
    assert validate('111.444 777-35') == '11144477735'
