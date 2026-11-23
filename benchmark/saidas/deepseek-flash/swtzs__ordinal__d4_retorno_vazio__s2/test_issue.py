import pytest

from alvo import ordinal


def test_non_numeric_string_is_returned_as_string():
    value = "something else"
    assert ordinal(value) == "something else"


def test_non_numeric_value_is_returned_using_str():
    assert ordinal(None) == "None"


def test_object_with_custom_str_is_returned_as_string():
    class NotNumeric:
        def __str__(self):
            return "not numeric"

    assert ordinal(NotNumeric()) == "not numeric"
