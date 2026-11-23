def test_c1_r2():
    # [R2/error]
    with pytest.raises(InvalidChecksum):
        validate('390.533.447-06')
