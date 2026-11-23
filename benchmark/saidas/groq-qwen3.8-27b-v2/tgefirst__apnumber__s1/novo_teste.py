def test_string_passthrough():
    # non-numeric strings pass through unchanged
    assert apnumber('hello') == 'hello'
    assert apnumber('123') == '123'