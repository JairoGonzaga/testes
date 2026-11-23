def test_punctuation_only_raises_invalid_format():
    # [R2/invalida]
    with pytest.raises(InvalidFormat):
        validate('...--')