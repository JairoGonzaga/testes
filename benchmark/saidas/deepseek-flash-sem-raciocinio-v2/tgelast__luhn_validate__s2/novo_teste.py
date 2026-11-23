

def test_c20_r6():
    # [R6/invalida]
    with pytest.raises(InvalidChecksum):
        validate('1a2b2', alphabet='0123456789abcdef')
