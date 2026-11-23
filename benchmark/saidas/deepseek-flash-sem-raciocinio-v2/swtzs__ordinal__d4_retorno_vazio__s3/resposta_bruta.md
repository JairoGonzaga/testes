Analysis:
- The issue states `ordinal('something else')` must return `'something else'` (the input as `str`).
- The current code returns `''` in the `except` branch, so the reproduction test on a non-numeric string fails now and passes after changing `return ''` to `return str(value)`.
- Only the string case from the issue is asserted; the expected value comes directly from the issue text.
- Related: `ordinal(None)`/unconvertible types—issue only promises non-numeric values return `str(value)`; keep focus on the given example plus one similar string.

```python
import pytest

from alvo import ordinal


def test_ordinal_returns_input_for_non_numeric_string():
    assert ordinal('something else') == 'something else'


def test_ordinal_returns_input_for_another_non_numeric_string():
    assert ordinal('abc') == 'abc'
```

---- revisão ----

Notes: Both assertions are stated by the issue (`str(value)` for non-numeric input, example `'something else'`), fail now due to the empty-string return, and pass with the minimal fix; no changes needed.

```python
from alvo import ordinal


def test_ordinal_returns_input_for_non_numeric_string():
    assert ordinal('something else') == 'something else'


def test_ordinal_returns_input_for_another_non_numeric_string():
    assert ordinal('abc') == 'abc'
```