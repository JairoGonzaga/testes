

def test_c27_r7_formato():
    # [R7/normal] CPF válido com separadores variados
    assert validate(' 111.111.111-11 ') == '11111111111'
    with pytest.raises(InvalidChecksum):
        validate('111.111.111-12')
