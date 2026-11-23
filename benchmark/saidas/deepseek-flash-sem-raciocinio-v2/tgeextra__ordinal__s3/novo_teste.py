

def test_c37_r3_r4_misto():
    # [R3/R4] conversão de diversos tipos e retorno de str em inválidos
    assert ordinal(' 7 ') == '7th'
    assert ordinal('3.9') == '3.9'
    assert ordinal(True) == '1st'
    assert ordinal('') == ''
    assert ordinal('21') == '21st'
    assert ordinal(1113) == '1113th'
