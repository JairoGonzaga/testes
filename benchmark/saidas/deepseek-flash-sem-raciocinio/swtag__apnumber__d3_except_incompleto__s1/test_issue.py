import pytest

from alvo import apnumber


def test_apnumber_none_returns_string():
    assert apnumber(None) == "None"


def test_apnumber_none_no_raise():
    try:
        result = apnumber(None)
    except TypeError as exc:  # pragma: no cover
        pytest.fail(f"apnumber(None) raised TypeError: {exc}")
    assert isinstance(result, str)


def test_apnumber_strings_unchanged():
    assert apnumber("abc") == "abc"


def test_apnumber_normal_values_still_work():
    assert apnumber(0) == "zero"
    assert apnumber(3) == "three"
    assert apnumber(9) == "nine"
    assert apnumber(10) == "10"
