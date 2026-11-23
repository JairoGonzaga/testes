

def test_c1_r2_potencias_e_arredondamento():
    # [R2/normal]
    assert intword(999) == '999'
    assert intword(1000) == '1.0 thousand'
    assert intword(1500) == '1.5 thousand'
    assert intword(1234567) == '1.2 million'
    assert intword(-2000000) == '-2.0 million'
    assert intword(4123456, format="%.2f") == '4.12 million'
    assert intword(999500) == '999.5 thousand'
    assert intword(999950000) == '1.0 billion'
    assert intword(10 ** 33) == '1.0 decillion'
    assert intword(10 ** 100) == '1.0 googol'


def test_c1_r3_nao_finitos_e_invalidos():
    # [R3/erro]
    assert intword(float('nan')) == 'NaN'
    assert intword(float('inf')) == '+Inf'
    assert intword(float('-inf')) == '-Inf'
    assert intword('abc') == 'abc'
    assert intword(None) == 'None'
