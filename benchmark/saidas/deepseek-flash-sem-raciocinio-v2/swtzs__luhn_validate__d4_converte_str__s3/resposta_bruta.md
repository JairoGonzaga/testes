Analysis:
- The issue promises: `validate()` returns the received value unchanged when valid.
- For the int `79927398713` (the Luhn example from the issue), the current code returns `'79927398713'` (a str).
- Expected value is the int `79927398713` itself, per the issue text.
- Test: call `validate(79927398713)` and assert the result is exactly the int (identity of type and value).
- Also check `validate` returns str for a valid str input unchanged.

```python
import pytest

from alvo import validate


def test_validate_int_returns_int():
    result = validate(79927398713)
    assert result == 79927398713
    assert isinstance(result, int)


def test_validate_str_returns_str_unchanged():
    result = validate("79927398713")
    assert result == "79927398713"
    assert isinstance(result, str)
```


---- revisão ----

Notes: Both assertions trace fine — the int case comes straight from the issue (`validate(79927398713)` must stay int), and the str case traces the code (`str(number)` unchanged), so I keep them; no changes needed.

```python
import pytest

from alvo import validate


def test_validate_int_returns_int():
    result = validate(79927398713)
    assert result == 79927398713
    assert isinstance(result, int)


def test_validate_str_returns_str_unchanged():
    result = validate("79927398713")
    assert result == "79927398713"
    assert isinstance(result, str)
```