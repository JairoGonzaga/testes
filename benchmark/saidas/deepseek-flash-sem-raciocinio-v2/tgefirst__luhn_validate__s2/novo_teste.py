

def test_c2_r1_checksum_invalido_retorna_original():
    # [R1] números com checksum válido retornam o próprio valor
    assert validate('79927398713') == '79927398713'
    assert validate('18') == '18'
    assert validate(18) == 18
    # [R1] checksum inválido
    with pytest.raises(InvalidChecksum):
        validate('36')
    # [R1] formato inválido
    with pytest.raises(InvalidFormat):
        validate('abc')
    # InvalidChecksum e InvalidFormat são subclasses de ValidationError
    assert issubclass(InvalidChecksum, ValidationError)
    assert issubclass(InvalidFormat, ValidationError)
