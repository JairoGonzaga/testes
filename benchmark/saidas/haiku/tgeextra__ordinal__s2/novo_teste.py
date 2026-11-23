def test_c37_r6_string_nao_finita():
    # [R6/invalida]
    assert ordinal('inf') == '+Inf'
    assert ordinal('-inf') == '-Inf'
    assert ordinal('nan') == 'NaN'
