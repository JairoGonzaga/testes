Analysis:
- The issue promises: any value that fails the int conversion (TypeError/ValueError) must be returned as `str(value)`.
- Current code returns `''` in the except branch — this is the bug.
- Expected value comes directly from the issue: `ordinal('something else')` should be `'something else'`.
- Closely related cases: `None` → `'None'`, a list → its `str(...)`, since the code path is the same except branch and the rule is `str(value)`.
- I'll keep tests to the issue's stated input plus a couple of same-branch cases whose expected value is `str(value)` per the stated rule.

```python
from alvo import ordinal


def test_non_numeric_string_returns_str_of_value():
    assert ordinal('something else') == 'something else'


def test_none_returns_str_of_value():
    assert ordinal(None) == str(None)


def test_list_returns_str_of_value():
    value = ['a', 'b']
    assert ordinal(value) == str(value)
```

---- revisão ----

Notes: All three assertions target the same `except` branch and expect `str(value)` per the issue text; `None` and the list are same-branch cases also covered by the stated rule, but to stay strictly minimal I'll keep only the issue's literal input and one clearly-stated same-rule case (`None` → `'None'` follows directly from `str(value)`).

```python
from alvo import ordinal


def test_non_numeric_string_returns_str_of_value():
    assert ordinal('something else') == 'something else'


def test_none_returns_str_of_value():
    assert ordinal(None) == 'None'
```