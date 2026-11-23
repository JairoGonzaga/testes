from alvo import apnumber


def test_apnumber_none_returns_string():
    assert apnumber(None) == "None"


def test_apnumber_string_abc_returns_string():
    assert apnumber("abc") == "abc"
