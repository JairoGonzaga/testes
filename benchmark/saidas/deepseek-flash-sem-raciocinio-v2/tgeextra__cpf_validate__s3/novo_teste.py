

def test_c28_r8():
    # [R8/normal] número inteiro não iterável continua dando InvalidFormat
    with pytest.raises(InvalidFormat):
        validate(39053344705)


def test_c29_r8():
    # [R8/normal] número composto só de zeros com tamanho válido é rejeitado
    with pytest.raises(InvalidFormat):
        validate('00000000000')


def test_c30_r8():
    # [R8/fronteira] InvalidLength também é um InvalidFormat
    with pytest.raises(InvalidFormat):
        validate('390533447051')
