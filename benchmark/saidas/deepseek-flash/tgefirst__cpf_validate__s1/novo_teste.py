def test_c2_r1():
    # [R2/erro] dígito verificador inválido
    with pytest.raises(InvalidChecksum):
        validate('390.533.447-06')
