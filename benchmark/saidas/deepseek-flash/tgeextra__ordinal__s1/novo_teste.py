def test_c37_r3_strings_numericas_nao_inteiras_e_nao_finitas():
    # [R3/R4/R6] strings numéricas que passam por float(), mas não por int()
    assert ordinal('3.9') == '3.9'
    assert ordinal('1e3') == '1e3'
    assert ordinal('inf') == '+Inf'
    assert ordinal('-inf') == '-Inf'
    assert ordinal('nan') == 'NaN'
