import pytest

from alvo import apnumber


def test_apnumber_none_returns_string():
    assert apnumber(None) == "None"


def test_apnumber_non_convertible_values_stringified():
    assert apnumber("abc") == "abc"
    assert apnumber(None) == "None"
    assert apnumber([1, 2]) == "[1, 2]"
    assert apnumber({"a": 1}) == "{'a': 1}"
    assert apnumber(object) == str(object)


@pytest.mark.parametrize("value", [None])
def test_apnumber_none_type_error_absent(value):
    result = apnumber(value)
    assert isinstance(result, str)
