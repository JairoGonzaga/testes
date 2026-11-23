from alvo import ordinal


def test_ordinal_non_numeric_string_returns_original():
    assert ordinal('something else') == 'something else'


def test_ordinal_none_returns_string_representation():
    assert ordinal(None) == str(None)


def test_ordinal_invalid_no_arguments_value():
    assert ordinal([1, 2]) == str([1, 2])
