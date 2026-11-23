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

## Issue: apnumber(0) is not spelled out

The docs say numbers from 0 to 9 are returned as words, but zero comes back as a digit string.

```python
>>> from alvo import apnumber
>>> apnumber(0)
'0'
```

Expected `'zero'`. Other single digits (e.g. `apnumber(5)` -> `'five'`) work fine.

## Source: alvo.py

```python
import math

_APNUMBER_WORDS = (
    "zero", "one", "two", "three", "four",
    "five", "six", "seven", "eight", "nine",
)


def _format_not_finite(value):
    if math.isnan(value):
        return "NaN"
    if math.isinf(value) and value < 0:
        return "-Inf"
    if math.isinf(value) and value > 0:
        return "+Inf"
    return ""


def apnumber(value):
    try:
        if not math.isfinite(float(value)):
            return _format_not_finite(float(value))
        value = int(value)
    except (TypeError, ValueError):
        return str(value)
    if not 0 < value < 10:
        return str(value)
    return _APNUMBER_WORDS[value]
```
