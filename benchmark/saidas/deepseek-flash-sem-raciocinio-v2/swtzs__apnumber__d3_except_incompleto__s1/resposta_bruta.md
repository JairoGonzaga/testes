Analysis:
- Promise: values that cannot be converted to int are returned as `str(value)`.
- `apnumber(None)`: `float(None)` raises `TypeError`, not caught -> crash. Expected `'None'` per issue.
- `apnumber('abc')` returns `'abc'` (already works, ValueError path).
- Expected values come directly from the issue: `'None'` for None, `'abc'` for 'abc'.
- A minimal fix would catch `TypeError` too (or similar), making both return string unchanged.

```python
import pytest

from alvo import apnumber


def test_apnumber_none_returns_string():
    assert apnumber(None) == "None"


def test_apnumber_non_numeric_string_returns_unchanged():
    assert apnumber("abc") == "abc"
```

---- revisão ----

Notes: `apnumber(None) == 'None'` is exactly the expected value stated in the issue (fails now via uncaught TypeError, passes after fix); `apnumber('abc') == 'abc'` is also stated by the issue ("the same way apnumber('abc') returns 'abc'") and is fine to keep as a related sanity case.

```python
import pytest

from alvo import apnumber


def test_apnumber_none_returns_string():
    assert apnumber(None) == "None"


def test_apnumber_non_numeric_string_returns_unchanged():
    assert apnumber("abc") == "abc"
```