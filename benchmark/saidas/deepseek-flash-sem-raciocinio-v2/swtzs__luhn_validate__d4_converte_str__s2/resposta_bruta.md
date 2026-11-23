Analysis:
- Issue: `validate()` must return the received value unchanged when valid; for int input it currently returns `str(number)`.
- `validate(79927398713)` must return the int `79927398713` (an `int`, not a `str`).
- Also the string case must still return the string `'79927398713'` unchanged.
- Expected values come directly from the issue text.
- The bug is in the final `return str(number)`.

```python
from alvo import validate


def test_validate_int_returns_int():
    result = validate(79927398713)
    assert result == 79927398713
    assert isinstance(result, int)


def test_validate_str_returns_str():
    result = validate('79927398713')
    assert result == '79927398713'
    assert isinstance(result, str)
```

---- revisão ----

Notes: The int-return and type assertion come directly from the issue (`validate(79927398713)` expected int `79927398713`); the str case isn't explicitly required by the issue but is the documented "unchanged" contract — it also passes on current code, so it's safe and doesn't cause a false failure. Keeping both is fine; the int test fails now and passes after fixing `return str(number)`.

```python
from alvo import validate


def test_validate_int_returns_int():
    result = validate(79927398713)
    assert result == 79927398713
    assert isinstance(result, int)


def test_validate_str_returns_str():
    result = validate('79927398713')
    assert result == '79927398713'
    assert isinstance(result, str)
```