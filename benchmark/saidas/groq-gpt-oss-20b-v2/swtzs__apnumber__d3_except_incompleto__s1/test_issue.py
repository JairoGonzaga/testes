# test_issue.py
import pytest
from alvo import apnumber


def test_apnumber_none_returns_string():
    """
    Passing None should return the string "None" instead of raising an exception.
    """
    assert apnumber(None) == "None"


def test_apnumber_non_numeric_string_returns_itself():
    """
    Non‑numeric strings are returned unchanged.
    """
    assert apnumber("abc") == "abc"
