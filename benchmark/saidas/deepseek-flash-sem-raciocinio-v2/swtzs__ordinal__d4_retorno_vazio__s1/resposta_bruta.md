Analysis:
- The issue states `ordinal('something else')` must return `'something else'` (i.e. `str(value)`), not `''`.
- The bug is in the `except (TypeError, ValueError)` branch which returns `''`.
- Expected value comes directly from the issue text: `'something else'`.
- A closely related case: any non-numeric string, e.g. `'abc'`, should also return `str(value)` = `'abc'`.
- Non-numeric non-string such as a list — `str(value)` would be `"[...]"`; issue doesn't state, so stick to strings only plus maybe `None`? Keep minimal: use string inputs as stated.

```python
from alvo import ordinal


def test_ordinal_non_numeric_string_returns_value():
    assert ordinal('something else') == 'something else'


def test_ordinal_another_non_numeric_string():
    assert ordinal('abc') == 'abc'
```

---- revisão ----

Notes: `'something else'` is stated by the issue; `'abc'` is a closely related non-numeric string whose expected value follows the same stated rule (return `str(value)`), both fail now (`''`) and pass after the fix.

```python
from alvo import ordinal


def test_ordinal_non_numeric_string_returns_value():
    assert ordinal('something else') == 'something else'


def test_ordinal_another_non_numeric_string():
    assert ordinal('abc') == 'abc'
```