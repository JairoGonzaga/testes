

def test_c45_r9_expoente_limitado():
    # [R9/fronteira] exp e' limitado a len(suffix); o sufixo maximo se repete
    assert naturalsize(2**110, binary=True) == '1024.0 QiB'
    assert naturalsize(-10**40) == '-10000000000.0 QB'
    assert naturalsize(10**40, format='%.0f') == '10000000000 QB'
