Analysis:
- The issue promises `apnumber(9)` returns `'nine'`, i.e. single digits 0–9 are spelled out.
- The module maps words for "zero".."nine" (indices 0..9), but the guard is `0 <= value < 9`, excluding 9.
- Expected value `'nine'` comes directly from the issue text.
- So a test asserting `apnumber(9) == 'nine'` fails now and passes when the bound becomes `<= 9` / `< 10`.
- Keep it small: one call with the exact input/output from the issue.

```python
from alvo import apnumber


def test_apnumber_nine_is_spelled_out():
    assert apnumber(9) == "nine"
```
```

---- revisão ----

Notes: The single assertion mirrors the issue exactly (`apnumber(9)` → `'nine'`), fails on current code due to the `< 9` bound, and passes with the minimal fix to include 9.

```python
from alvo import apnumber


def test_apnumber_nine_is_spelled_out():
    assert apnumber(9) == "nine"
```