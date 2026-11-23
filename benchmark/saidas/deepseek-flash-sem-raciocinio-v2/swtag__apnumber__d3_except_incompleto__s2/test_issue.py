import pytest

from alvo import apnumber


def test_apnumber_none_returns_none_string():
    assert apnumber(None) == "None"


def test_apnumber_none_does_not_raise():
    try:
        apnumber(None)
    except TypeError as exc:  # pragma: no cover
        pytest.fail(f"apnumber(None) raised TypeError: {exc}")


def test_non_numeric_objects_still_returned_as_string():
    class Foo:
        def __str__(self):
            return "foo"

        def __float__(self):
            raise TypeError("nope")

    assert apnumber(Foo()) == "foo"
