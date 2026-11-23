from alvo import ordinal


def test_non_numeric_string_returns_str_of_value():
    assert ordinal('something else') == 'something else'


def test_none_returns_str_of_value():
    assert ordinal(None) == 'None'
