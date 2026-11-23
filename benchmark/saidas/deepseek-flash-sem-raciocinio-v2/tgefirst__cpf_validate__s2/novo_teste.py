

def test_c1_r2():
    # [R1/erros]
    with pytest.raises(InvalidFormat):
        validate('390.533.447-0a')
    with pytest.raises(InvalidLength):
        validate('390.533.447-055')
    with pytest.raises(InvalidChecksum):
        validate('390.533.447-06')
    with pytest.raises(ValidationError):
        validate('000.000.000-00')
    with pytest.raises(InvalidFormat):
        validate('')
