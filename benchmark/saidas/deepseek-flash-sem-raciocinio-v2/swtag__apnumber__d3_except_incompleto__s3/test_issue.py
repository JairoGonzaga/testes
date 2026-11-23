from alvo import apnumber


def test_apnumber_none_returns_none_string():
    assert apnumber(None) == "None"


def test_apnumber_non_convertible_string_unchanged():
    assert apnumber("abc") == "abc"


def test_apnumber_basic_behaviour_still_works():
    assert apnumber(3) == "three"
    assert apnumber("7") == "seven"
