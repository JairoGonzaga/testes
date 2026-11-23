

def test_c20_r6():
    # [R6/invalida]
    with pytest.raises(InvalidChecksum):
        validate('2', alphabet='1098765432')
