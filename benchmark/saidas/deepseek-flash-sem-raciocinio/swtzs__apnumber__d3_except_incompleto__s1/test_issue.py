import math

import pytest

from alvo import apnumber


def test_apnumber_none_returns_string():
    assert apnumber(None) == "None"


def test_apnumber_non_numeric_string_returns_unchanged():
    assert apnumber("abc") == "abc"


def test_apnumber_none_matches_other_unconvertible_values():
    assert apnumber(None) == str(None)


def test_apnumber_none_does_not_raise_type_error():
    try:
        result = apnumber(None)
    except TypeError as exc:
        pytest.fail(f"apnumber(None) raised TypeError: {exc}")
    assert result == "None"
