def test_c27_r7():
    # [R7/normal]
    for d in '123456789':
        assert validate(d * 3 + '.' + d * 3 + '.' + d * 3 + '-' + d * 2) == d * 11
