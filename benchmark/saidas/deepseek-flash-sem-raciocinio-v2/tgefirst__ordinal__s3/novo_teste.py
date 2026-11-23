

def test_c2_r1_ordinal_nao_finito_e_teens():
    # [R1/nao finito]
    assert ordinal(float('nan')) == 'NaN'
    assert ordinal(float('inf')) == '+Inf'
    assert ordinal(float('-inf')) == '-Inf'
    # [R1/excecoes]
    assert ordinal('abc') == 'abc'
    assert ordinal('3.9') == '3.9'
    assert ordinal(None) == 'None'
    # [R1/teens e dezenas]
    assert ordinal(11) == '11th'
    assert ordinal(12) == '12th'
    assert ordinal(13) == '13th'
    assert ordinal(21) == '21st'
    assert ordinal(22) == '22nd'
    assert ordinal(23) == '23rd'
    assert ordinal(4) == '4th'
    assert ordinal(111) == '111th'
    assert ordinal(112) == '112th'
    assert ordinal(113) == '113th'
    assert ordinal(101) == '101st'


def test_c3_r1_truncamento_e_sufixo_zero():
    # [R1/truncamento para inteiro]
    assert ordinal(1.9) == '1st'
    assert ordinal(3.9) == '3rd'
    assert ordinal(True) == '1st'
    # [R1/digito zero]
    assert ordinal(0) == '0th'
    assert ordinal(100) == '100th'
