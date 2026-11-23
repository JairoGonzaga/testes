

def test_c21_alphabet_custom():
    # [R6/fronteira] maiúsculas não pertencem ao alfabeto
    with pytest.raises(InvalidFormat):
        validate('1A2B1', alphabet='0123456789abcdef')
    assert validate('1010', alphabet='01') == '1010'
