from alvo import apnumber


def test_apnumber_none_returns_string_representation():
    # Passing None raises TypeError today; the fix should return str(None).
    assert apnumber(None) == "None"


def test_apnumber_non_numeric_string_returns_unchanged():
    # Stated contrast in the issue: non-numeric strings are returned unchanged.
    assert apnumber("abc") == "abc"
