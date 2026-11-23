def test_c45_r8():
    # [R8/fronteira] arredondamento que sobe a unidade tambem com sinal negativo
    assert naturalsize(-999999) == '-1.0 MB'
    assert naturalsize(-1048575, binary=True) == '-1.0 MiB'
