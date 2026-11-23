def test_c1_r2():
    # [R1/erros] Formato, comprimento e dígito verificador inválidos.
    with pytest.raises(InvalidFormat):
        validate('390.533.447-0a')
    with pytest.raises(InvalidLength):
        validate('390.533.447-0')
    with pytest.raises(InvalidChecksum):
        validate('390.533.447-04')
