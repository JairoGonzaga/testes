

def test_c37_r3_r6_varios():
    # [R3/R6/outros]
    assert ordinal('inf') == '+Inf'
    assert ordinal('-inf') == '-Inf'
    assert ordinal('nan') == 'NaN'
    assert ordinal(1.0) == '1st'
    assert ordinal(100) == '100th'
    assert ordinal(-1) == '-1th'
    assert ordinal(-112) == '-112th'
    assert ordinal('  7  ') == '7th'
    assert ordinal('3.9') == '3.9'
    assert ordinal({'a': 1}) == "{'a': 1}"
