def test_c1_r2():
    # [R2/negative]
    assert intword(-1) == '-1'
    assert intword(-999) == '-999'
    assert intword(-1000) == '-1.0 thousand'
    assert intword(-1500000) == '-1.5 million'
