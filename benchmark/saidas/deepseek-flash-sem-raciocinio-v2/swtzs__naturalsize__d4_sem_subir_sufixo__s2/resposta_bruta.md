## Analysis

The issue states `naturalsize(999999)` currently returns `'1000.0 kB'` but should return `'1.0 MB'`, and the general promise: when rounding pushes the value to the next unit's size (1000.0 in decimal / 1024.0 in binary), the unit must be promoted one step.

Expected values come directly from the issue text: `naturalsize(999999) == '1.0 MB'`.

Tracing the code: base=1000, exp = int(log(999999, 1000)) = 1 → `format % (999999/1000)` = `'1000.0'` + `' '` + `'kB'` → `'1000.0 kB'`. Fix must detect the rounded display equals the base and bump exp.

Binary analogy (not stated by issue) is avoided to stay minimal; only closely related decimal cases whose expected value follows from the stated promotion rule are included.

```python
from alvo import naturalsize


def test_naturalsize_999999_returns_1_mb():
    # Reported in the issue: rounding to 1000.0 must promote to next unit.
    assert naturalsize(999999) == "1.0 MB"


def test_naturalsize_just_below_1mb_is_kb():
    # Not promoted: still within the kB range.
    assert naturalsize(999000) == "999.0 kB"


def test_naturalsize_999_returns_bytes():
    assert naturalsize(999) == "999 Bytes"
```

---- revisão ----

Notes: Keep only `naturalsize(999999) == '1.0 MB'` (stated in the issue); drop `999000` and `999` cases since their expected values are not stated by the issue and are only my assumptions about formatting thresholds.

```python
from alvo import naturalsize


def test_naturalsize_999999_returns_1_mb():
    # Reported in the issue: rounding to 1000.0 must promote to the next unit.
    assert naturalsize(999999) == "1.0 MB"
```