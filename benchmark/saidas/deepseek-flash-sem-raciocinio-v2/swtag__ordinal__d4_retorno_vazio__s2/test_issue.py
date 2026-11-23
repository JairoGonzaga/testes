from alvo import ordinal


def test_non_numeric_string_returns_str_value():
    assert ordinal('something else') == 'something else'


def test_none_returns_str_value():
    assert ordinal(None) == 'None'


def test_numeric_still_works():
    assert ordinal(1) == '1st'
    assert ordinal(2) == '2nd'
    assert ordinal(11) == '11th'
