def test_c45_r8_rounding_cascade():
    # [R8/fronteira] arredondamento empurra a exponente para a próxima unidade
    assert naturalsize(999950) == '1.0 MB'
    assert naturalsize(999949) == '999.9 kB'
