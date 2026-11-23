**Analysis:**
- The issue promises: any value that cannot be converted to `int` is returned as `str(value)`.
- `apnumber('abc')` → `'abc'` is the stated reference behaviour (ValueError path).
- `apnumber(None)`: `float(None)` raises `TypeError`, which the `except ValueError` clause does not catch, so it crashes.
- Expected after fix: `apnumber(None) == 'None'`, per the issue text.
- The issue also says "values that cannot be converted to int"—so `None` is the only concrete case stated; we test it directly and confirm the reference `'abc'` case.

```python
import pytest

from alvo import apnumber


def test_apnumber_none_returns_string():
    assert apnumber(None) == "None"


def test_apnumber_string_abc_returns_string():
    assert apnumber("abc") == "abc"
```

---- revisão ----

Notes: `apnumber(None) == 'None'` is the exact expected value stated in the issue; `apnumber('abc') == 'abc'` is the reference behaviour stated in the issue ("the same way apnumber('abc') returns 'abc'"). Both checks pass and the first fails only due to the TypeError bug.

```python
from alvo import apnumber


def test_apnumber_none_returns_string():
    assert apnumber(None) == "None"


def test_apnumber_string_abc_returns_string():
    assert apnumber("abc") == "abc"
```