Below is the source code of a Python module, `alvo.py`.

Write a complete pytest unit-test suite for this module.
- Import with `from alvo import ...`. The test file will be saved as `test_alvo.py` next to `alvo.py`.
- The tests must pass on this code.
- Exercise all of its behaviour (aim for full line and branch coverage), including edge cases and
  error handling, and make the assertions strong enough to catch bugs: the suite will be evaluated
  by coverage and by mutation testing.
- The answer is a single complete, runnable pytest file.

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
        return str(value)
    digit = 0 if value % 100 in (11, 12, 13) else value % 10
    return f"{value}{_SUFIXOS[digit]}"
```
