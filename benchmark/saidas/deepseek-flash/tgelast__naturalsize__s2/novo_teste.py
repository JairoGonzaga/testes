def test_c44_r8():
    # [R8/fronteira]
    assert naturalsize(1048575, binary=True) == '1.0 MiB'
    assert naturalsize(1048575, gnu=True) == '1.0M'
    assert naturalsize(-999999) == '-1.0 MB'
