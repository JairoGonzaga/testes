from alvo import ordinal


def test_ordinal_returns_input_for_non_numeric_string():
    assert ordinal('something else') == 'something else'


def test_ordinal_returns_input_for_another_non_numeric_string():
    assert ordinal('abc') == 'abc'
