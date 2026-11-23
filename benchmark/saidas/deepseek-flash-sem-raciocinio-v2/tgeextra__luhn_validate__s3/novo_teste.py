

def test_c21_r6_alfabeto_hexadecimal():
    # [R6/normal] alfabeto hexadecimal: 'ab' tem checksum zero, 'ba' não
    assert validate('ab', alphabet='0123456789abcdef') == 'ab'
    with pytest.raises(InvalidChecksum):
        validate('ba', alphabet='0123456789abcdef')
    # o mesmo valor 'ab' não existe no alfabeto padrão
    with pytest.raises(InvalidFormat):
        validate('ab')
