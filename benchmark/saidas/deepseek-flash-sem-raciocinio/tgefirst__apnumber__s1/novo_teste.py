def test_c1_r1_negative_non_finite():
    # [R1/fronteira] valores não finitos negativos ou NaN
    assert apnumber(-math.inf) == '-Inf'
    assert apnumber(math.nan) == 'NaN'
