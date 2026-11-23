def test_c2_invalid_format():
    # Invalid: non-digit characters after cleaning
    with pytest.raises(InvalidFormat):
        validate('abc')

    # Invalid: all zeros (int(value) <= 0)
    with pytest.raises(InvalidFormat):
        validate('000.000.000-00')

    # Invalid: too short
    with pytest.raises(InvalidLength):
        validate('123')

    # Invalid: checksum mismatch
    with pytest.raises(InvalidChecksum):
        validate('12345678900')

    # Valid: with formatting
    assert validate('100.000.000-19') == '10000000019'

    # Valid: plain digits
    assert validate('12345678909') == '12345678909'