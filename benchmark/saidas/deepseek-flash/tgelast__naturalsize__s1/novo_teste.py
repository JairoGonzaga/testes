def test_c44_r8():
    # [R8/fronteira] arredondamento para a próxima unidade, inclusive no limite de sufixos
    assert naturalsize(1048575, binary=True) == "1.0 MiB"
    assert naturalsize(1048575, gnu=True) == "1.0M"
    assert naturalsize(-999999) == "-1.0 MB"
    assert naturalsize(10**33) == "1000.0 QB"
