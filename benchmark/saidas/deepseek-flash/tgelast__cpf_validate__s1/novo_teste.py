def test_c27_r7():
    # [R7/fronteira]
    for digit in "123456789":
        raw = digit * 11
        assert validate(raw) == raw
        formatted = f"{digit * 3}.{digit * 3}.{digit * 3}-{digit * 2}"
        assert validate(formatted) == raw
