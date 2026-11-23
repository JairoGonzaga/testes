def test_c36_r6_nan():
    # [R6/invalida]
    assert ordinal(float('nan')) == 'NaN'
