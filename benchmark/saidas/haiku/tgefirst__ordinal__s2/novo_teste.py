def test_c1_r2():
    # [R2/special]
    assert ordinal(11) == '11th'
    assert ordinal(12) == '12th'
    assert ordinal(13) == '13th'
    assert ordinal(111) == '111th'
