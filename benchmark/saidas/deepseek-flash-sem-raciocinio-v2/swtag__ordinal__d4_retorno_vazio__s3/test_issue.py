from alvo import ordinal


def test_non_numeric_string_returns_str_value():
    assert ordinal('something else') == 'something else'


def test_other_non_convertible_values_return_str_value():
    assert ordinal('abc') == 'abc'
    assert ordinal('2.7') == '2.7'
    assert ordinal(None) == 'None'
    assert ordinal([1, 2]) == '[1, 2]'


def test_numeric_behaviour_unchanged():
    assert ordinal(3) == '3rd'
    assert ordinal('11') == '11th'
    assert ordinal(2.7) == '2nd'
