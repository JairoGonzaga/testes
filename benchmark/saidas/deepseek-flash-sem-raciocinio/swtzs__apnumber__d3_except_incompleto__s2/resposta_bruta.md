```python
import math

import pytest

from alvo import apnumber


def test_apnumber_none_returns_string():
    assert apnumber(None) == "None"


def test_apnumber_none_does_not_raise_type_error():
    try:
        result = apnumber(None)
    except TypeError as exc:  # pragma: no cover - only on buggy code
        pytest.fail(f"apnumber(None) raised TypeError: {exc}")
    assert isinstance(result, str)


def test_non_convertible_strings_still_unchanged():
    assert apnumber("abc") == "abc"


def test_non_finite_float_unchanged_behavior():
    assert apnumber(float("nan")) == "NaN"
    assert apnumber(float("inf")) == "+Inf"
    assert apnumber(float("-inf")) == "-Inf"


def test_non_convertible_objects_become_str():
    class Foo:
        def __str__(self):
            return "foo-object"

        def __float__(self):
            raise ValueError("nope")

    assert apnumber(Foo()) == "foo-object"
```