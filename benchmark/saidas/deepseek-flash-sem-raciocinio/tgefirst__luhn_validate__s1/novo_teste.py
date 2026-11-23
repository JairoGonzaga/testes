def test_c2_r1():
    # [R1/fronteira] caracteres fora do alfabeto
    with pytest.raises(InvalidFormat):
        validate('abc')
