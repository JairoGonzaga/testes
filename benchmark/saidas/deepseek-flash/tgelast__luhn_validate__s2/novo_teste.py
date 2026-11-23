def test_c20_r7():
    # [R7/invalida]
    with pytest.raises(InvalidFormat):
        validate(math.inf)
