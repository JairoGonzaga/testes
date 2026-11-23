

def test_c20_r6_invalida():
    # [R6/invalida]
    with pytest.raises(ValidationError):
        validate('1a2b', alphabet='0123456789abcdef')
