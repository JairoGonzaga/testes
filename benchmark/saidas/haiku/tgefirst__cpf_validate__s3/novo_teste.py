def test_c1_r2():
    # [R2/erro]
    with pytest.raises(InvalidChecksum) as excinfo:
        validate('390.533.447-06')
    assert isinstance(excinfo.value, ValidationError)
