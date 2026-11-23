def test_c45_r8_arredondamento_binario():
    # [R8/fronteira]
    assert naturalsize(1048575, binary=True) == '1.0 MiB'
    assert naturalsize(-1048575, binary=True) == '-1.0 MiB'
    assert naturalsize(1048575, gnu=True) == '1.0M'
