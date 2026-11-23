

def test_c2_r2():
    # [R2/fronteira]
    assert validate('0') == '0'
    assert validate('18') == '18'
    with pytest.raises(InvalidChecksum):
        validate('1')
    with pytest.raises(InvalidChecksum):
        validate('12345678')
    with pytest.raises(InvalidFormat):
        validate(0)
    with pytest.raises(InvalidFormat):
        validate('12a')
