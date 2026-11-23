```python
from alvo import apnumber

def test_apnumber_none_returns_string_none():
    # Issue states apnumber(None) must return 'None' like apnumber('abc') -> 'abc'
    assert apnumber(None) == 'None'

def test_apnumber_abc_returns_unchanged():
    assert apnumber('abc') == 'abc'
```

---- revisão ----

Notes: `apnumber(None) == 'None'` is exactly the issue's expected value and fails on current code only due to the uncaught `TypeError`; the `'abc'` assertion is stated by the issue and passes on current code, so keep both.

```python
from alvo import apnumber

def test_apnumber_none_returns_string_none():
    # Issue explicitly states apnumber(None) must return 'None'
    assert apnumber(None) == 'None'

def test_apnumber_abc_returns_unchanged():
    # Issue states apnumber('abc') returns 'abc'
    assert apnumber('abc') == 'abc'
```