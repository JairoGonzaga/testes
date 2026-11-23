## Analysis

The issue states `apnumber(0)` should return `'zero'` (docs: 0–9 as words), but currently returns `'0'`.

Tracing the code: after `value = int(value)`, the guard is `if not 0 < value < 10: return str(value)`. For `value == 0`, `0 < 0` is False, so `not False` is True → returns `str(0)` = `'0'`. That's the bug.

Expected values come from the issue:
- `apnumber(0)` → `'zero'` (fix: guard must include 0, e.g. `0 <= value < 10`)
- `apnumber(5)` → `'five'` (already working; the issue states this as correct)

I'll also assert the neighbouring boundary behaviour stated by the issue's "0 to 9" range: `apnumber(9)` → `'nine'` (also already passing, included as a closely related case, safe since code returns `_APNUMBER_WORDS[9]`). Keep it small.

```python
from alvo import apnumber


def test_apnumber_zero_is_word():
    # Issue: zero comes back as digit string; expected 'zero'.
    assert apnumber(0) == "zero"


def test_apnumber_five_is_word():
    # Issue explicitly says single digits like 5 already work.
    assert apnumber(5) == "five"


def test_apnumber_nine_is_word():
    # "0 to 9" range: nine is the upper bound of the word range.
    assert apnumber(9) == "nine"
```

---- revisão ----

Notes: `apnumber(0)=='zero'` is from the issue and fails only due to the `0 < value` guard bug (passes with `0 <= value`); `apnumber(5)=='five'` and `apnumber(9)=='nine'` are trace-verified against the given code (5 and 9 are within `0 < value < 10`, so they pass now and after the fix) — all kept.

```python
from alvo import apnumber


def test_apnumber_zero_is_word():
    # Issue: zero comes back as digit string; expected 'zero'.
    assert apnumber(0) == "zero"


def test_apnumber_five_is_word():
    # Issue explicitly says single digits like 5 already work.
    assert apnumber(5) == "five"


def test_apnumber_nine_is_word():
    # "0 to 9" range: nine is the upper bound of the word range.
    assert apnumber(9) == "nine"
```