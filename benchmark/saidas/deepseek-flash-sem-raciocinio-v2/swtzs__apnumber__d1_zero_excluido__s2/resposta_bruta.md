Analysis:
- Promise: `apnumber` returns words for integers 0–9, per issue. `apnumber(0)` must be `'zero'`.
- Expected values come directly from the issue text: `apnumber(0) == 'zero'`, and the issue states `apnumber(5) == 'five'` works.
- Bug: guard `if not 0 < value < 10` excludes 0, so it returns `str(0)` -> `'0'`.
- Fix is presumably `0 <= value < 10`; test only checks the stated case(s), not the fix.
- Use `apnumber(0)` (issue input) and one related stated case `apnumber(5)`.
- Keep small: exactly the reproducer and the stated working case.

```python
from alvo import apnumber


def test_apnumber_zero_is_spelled_out():
    assert apnumber(0) == "zero"


def test_apnumber_five_still_spelled_out():
    assert apnumber(5) == "five"
```

---- revisão ----

Notes: Both assertions are safe — `apnumber(0)=='zero'` is the issue's expected value (fails now due to the `0 < value` guard), and `apnumber(5)=='five'` is the issue's stated working case taken verbatim; both pass after the minimal `0 <=` fix.

```python
from alvo import apnumber


def test_apnumber_zero_is_spelled_out():
    assert apnumber(0) == "zero"


def test_apnumber_five_still_spelled_out():
    assert apnumber(5) == "five"
```