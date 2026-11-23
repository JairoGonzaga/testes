from alvo import ordinal


def test_ordinal_non_numeric_string_returns_value():
    assert ordinal('something else') == 'something else'


def test_ordinal_another_non_numeric_string():
    assert ordinal('abc') == 'abc'
