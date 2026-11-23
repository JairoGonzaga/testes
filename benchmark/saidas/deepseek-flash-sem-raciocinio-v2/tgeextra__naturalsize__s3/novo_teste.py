

def test_c45_r8_arredondamento():
    # [R8/fronteira] arredondamento do format faz subir de expoente
    assert naturalsize(1024 * 1024 - 1, binary=True) == '1.0 MiB'
    assert naturalsize(1024 * 1024 * 1024 * 1024 * 1024 * 1024 * 1024 * 1024 * 1024 * 1024 * 1000,
                       binary=True) == '1000.0 QiB'
