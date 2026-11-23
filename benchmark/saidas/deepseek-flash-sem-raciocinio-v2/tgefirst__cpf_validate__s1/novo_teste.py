

def test_l1_curto():
    # [L1/erro] comprimento errado
    with pytest.raises(InvalidLength):
        validate('3905334470')


def test_l2_longo():
    # [L2/erro] comprimento errado
    with pytest.raises(InvalidLength):
        validate('390533447050')


def test_c2_r2():
    # [R2/erro] dígito verificador errado
    with pytest.raises(InvalidChecksum):
        validate('390.533.447-06')
    assert issubclass(InvalidLength, InvalidFormat)
    assert issubclass(ValidationError, ValueError)
    assert math.isclose(1.0, 1.0)


def test_c3_r3():
    # [R3/erro] formato inválido
    with pytest.raises(InvalidFormat):
        validate('3905334470a')
    with pytest.raises(InvalidFormat):
        validate('00000000000')
