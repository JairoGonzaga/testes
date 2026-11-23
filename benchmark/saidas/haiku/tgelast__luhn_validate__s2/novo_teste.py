def test_c20_r2():
    # [R2/invalida]
    with pytest.raises(InvalidFormat):
        validate(math.inf)
