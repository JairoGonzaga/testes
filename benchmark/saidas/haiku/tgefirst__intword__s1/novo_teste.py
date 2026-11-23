def test_c1_r2():
    # [R2/boundary]
    assert intword(999999999) == '1.0 billion'
    assert intword(-999999999) == '-1.0 billion'
