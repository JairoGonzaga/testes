def test_c37_r6_strings_nao_finitas():
    # [R6/invalida]
    assert ordinal('nan') == 'NaN'
    assert ordinal('inf') == '+Inf'
    assert ordinal('-Infinity') == '-Inf'
