def test_c1_r2():
    # [R2/normal]
    assert ordinal(2) == '2nd'
    assert ordinal(3) == '3rd'
    assert ordinal(21) == '21st'
    assert ordinal(112) == '112th'
