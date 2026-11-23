```python
from alvo import apnumber


def test_apnumber_none_returns_string():
    assert apnumber(None) == "None"


def test_apnumber_none_does_not_raise_type_error():
    try:
        result = apnumber(None)
    except TypeError as exc:
        raise AssertionError(f"apnumber(None) raised TypeError: {exc}") from exc

    assert result == str(None)
```