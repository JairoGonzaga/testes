def test_c2_r1():
    # [R1/checksum]
    with pytest.raises(InvalidChecksum):
        validate('79927398710')
