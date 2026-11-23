def test_c20_r4():
    # [R4/invalida]
    with pytest.raises(ValidationError):
        validate('1a2b2', alphabet='0123456789abcdef')
