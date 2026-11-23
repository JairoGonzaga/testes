You are given an issue report for a small Python project and the full source of the module it
concerns, `alvo.py`.

Write a pytest test file that REPRODUCES the issue:
- the tests must FAIL on the current code (because of the bug described in the issue), and
- the tests must PASS once the issue is fixed.

Rules:
- Import from the module with `from alvo import ...`. The test file will be saved as
  `test_issue.py` in the same folder as `alvo.py`.
- Do not modify, copy or re-implement the module. Do not fix the bug.
- The answer is a single complete, runnable pytest file.

## Issue: ordinal() returns an empty string for non-numeric input

Values that cannot be converted to int should be returned as `str(value)`, but an empty string comes back:

```python
>>> from alvo import ordinal
>>> ordinal('something else')
''
```

Expected `'something else'`.

## Source: alvo.py

```python
import math

_SUFIXOS = ("th", "st", "nd", "rd", "th", "th", "th", "th", "th", "th")


def _format_not_finite(value):
    if math.isnan(value):
        return "NaN"
    if math.isinf(value) and value < 0:
        return "-Inf"
    if math.isinf(value) and value > 0:
        return "+Inf"
    return ""


def ordinal(value, gender="male"):
    try:
        if not math.isfinite(float(value)):
            return _format_not_finite(float(value))
        value = int(value)
    except (TypeError, ValueError):
        return ''
    digit = 0 if value % 100 in (11, 12, 13) else value % 10
    return f"{value}{_SUFIXOS[digit]}"
```
