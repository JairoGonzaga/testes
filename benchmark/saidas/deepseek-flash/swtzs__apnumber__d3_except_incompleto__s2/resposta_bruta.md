```python
from alvo import apnumber


def test_apnumber_none_returns_string_unchanged():
    assert apnumber(None) == "None"


def test_apnumber_non_numeric_string_returns_string_unchanged():
    assert apnumber("abc") == "abc"
```