def test_c37_r4_r6():
    # [R4/invalida] float válido, mas conversão para int inválida
    assert ordinal('3.9') == '3.9'

    # [R6/invalida] valores não finitos passados como string
    assert ordinal('inf') == '+Inf'
    assert ordinal('-inf') == '-Inf'
    assert ordinal('nan') == 'NaN'
