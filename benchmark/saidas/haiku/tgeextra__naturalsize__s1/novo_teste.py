def test_c45_r4():
    # [R4/fronteira]
    # Arredondamento que estoura a unidade tambem vale para valores negativos
    assert naturalsize(-999999) == '-1.0 MB'
    # Mesmo efeito no sistema binario: 1048575 / 1024 arredonda para 1024.0 e sobe para MiB
    assert naturalsize(1048575, binary=True) == '1.0 MiB'
