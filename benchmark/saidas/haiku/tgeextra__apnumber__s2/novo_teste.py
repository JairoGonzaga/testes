def test_c23_r5_string_nao_finita():
    # [R5/invalida]
    # Strings de infinito/NaN passam por float() e saem no formato de nao finito,
    # e nao como o texto original.
    assert apnumber('inf') == '+Inf'
    assert apnumber('-Infinity') == '-Inf'
    assert apnumber('NAN') == 'NaN'
