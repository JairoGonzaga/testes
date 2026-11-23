from alvo import ordinal


def test_non_numeric_string_is_returned_as_is():
    assert ordinal("something else") == "something else"


def test_other_non_numeric_values_are_returned_as_str():
    assert ordinal("abc") == "abc"
    assert ordinal("x") == "x"
    assert ordinal(None) == "None"


def test_non_numeric_value_with_gender_argument():
    assert ordinal("something else", gender="female") == "something else"


def test_valid_inputs_still_work():
    assert ordinal(3) == "3rd"
    assert ordinal("2") == "2nd"
    assert ordinal(11) == "11th"
