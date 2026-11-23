def test_c44_r8():
    # [R8/normal]
    assert naturalsize(999999999) == '1.0 GB'
    assert naturalsize(1048575, binary=True) == '1.0 MiB'
