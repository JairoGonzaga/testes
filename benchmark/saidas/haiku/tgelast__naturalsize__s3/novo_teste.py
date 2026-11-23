def test_c44_r8():
    # [R8/fronteira]
    assert naturalsize(1048575, binary=True) == '1.0 MiB'
