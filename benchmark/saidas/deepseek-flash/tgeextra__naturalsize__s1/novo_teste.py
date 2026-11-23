def test_c45_r8():
    # [R8/fronteira] arredondamento deve avançar para o último sufixo
    assert naturalsize(999999 * 1000**8) == '1.0 QB'
