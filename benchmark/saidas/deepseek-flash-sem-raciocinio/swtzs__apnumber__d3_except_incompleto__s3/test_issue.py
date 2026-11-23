import pytest

from alvo import apnumber


def test_apnumber_none_returns_string_none():
    assert apnumber(None) == "None"


def test_apnumber_none_does_not_raise():
    try:
        result = apnumber(None)
    except TypeError as exc:
        pytest.fail(f"apnumber(None) raised TypeError: {exc}")
    assert result == "None"


def test_apnumber_non_numeric_string_unchanged():
    # Sanity check that strings are returned unchanged, matching the issue's
    # expectation for None.
    assert apnumber("abc") == "abc"


def test_apnumber_object_without_int_conversion():
    class Unconvertible:
        pass

    obj = Unconvertible()
    assert apnumber(obj) == str(obj)
