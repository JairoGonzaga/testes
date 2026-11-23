

def test_c21_checksum_contrato_publico():
    # [checksum/fronteira e heranca de excecoes]
    from alvo import checksum

    assert checksum('79927398713') == 0
    assert checksum(79927398713) == 0
    assert checksum('79927398710') == 7
    assert checksum('18') == 0
    assert checksum('0') == 0
    assert checksum('1a2b1', alphabet='0123456789abcdef') == 0
    assert issubclass(InvalidFormat, ValidationError)
    assert issubclass(InvalidChecksum, ValidationError)
