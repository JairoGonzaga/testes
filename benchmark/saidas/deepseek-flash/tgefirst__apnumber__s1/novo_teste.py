def test_c2_r1():
    # [R1/fronteira e não finitos]
    assert apnumber(1) == 'one'
    assert apnumber(9) == 'nine'
    assert apnumber(10) == '10'
    assert apnumber(-1) == '-1'
    assert apnumber(math.nan) == 'NaN'
    assert apnumber(math.inf) == '+Inf'
    assert apnumber(-math.inf) == '-Inf'
