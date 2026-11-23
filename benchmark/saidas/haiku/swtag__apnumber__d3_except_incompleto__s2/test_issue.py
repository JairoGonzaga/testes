from alvo import apnumber


def test_none_returns_str_none():
    # Issue: apnumber(None) raises TypeError instead of returning 'None'.
    assert apnumber(None) == "None"


def test_none_matches_non_numeric_string_behaviour():
    # Non-convertible values are returned as str(value), like apnumber('abc').
    assert apnumber("abc") == "abc"
    assert apnumber(None) == str(None)


def test_list_returns_str_of_list():
    # Another value that cannot be converted to int must also be returned as str.
    assert apnumber([1, 2]) == str([1, 2])


def test_object_returns_its_str():
    class Custom:
        def __str__(self):
            return "custom-value"

    assert apnumber(Custom()) == "custom-value"
