

def test_c2_r2_nao_finitos_e_invalidos():
    # [R2/exceções e não finitos]
    assert ordinal(float('nan')) == 'NaN'
    assert ordinal(float('inf')) == '+Inf'
    assert ordinal(float('-inf')) == '-Inf'
    assert ordinal('abc') == 'abc'
    assert ordinal('3.9') == '3.9'
    assert ordinal([1]) == '[1]'


def test_c3_r1_sufixos_especiais():
    # [R1/normal]
    assert ordinal(0) == '0th'
    assert ordinal(2) == '2nd'
    assert ordinal(3) == '3rd'
    assert ordinal(4) == '4th'
    assert ordinal(11) == '11th'
    assert ordinal(12) == '12th'
    assert ordinal(13) == '13th'
    assert ordinal(21) == '21st'
    assert ordinal(22) == '22nd'
    assert ordinal(23) == '23rd'
    assert ordinal(101) == '101st'
    assert ordinal(111) == '111th'
    assert ordinal(112) == '112th'
    assert ordinal(113) == '113th'
    assert ordinal(1.0) == '1st'
    assert ordinal(2.7) == '2nd'
