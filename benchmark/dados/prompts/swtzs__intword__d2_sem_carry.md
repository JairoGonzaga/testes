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

## Issue: intword(999999) returns '1000.0 thousand'

When rounding pushes a value up to the next power, the suffix is not promoted:

```python
>>> from alvo import intword
>>> intword(999999)
'1000.0 thousand'
```

Expected `'1.0 million'`.

## Source: alvo.py

```python
import bisect
import math

powers = [10**x for x in (3, 6, 9, 12, 15, 18, 21, 24, 27, 30, 33, 100)]
human_powers = (
    "thousand", "million", "billion", "trillion", "quadrillion", "quintillion",
    "sextillion", "septillion", "octillion", "nonillion", "decillion", "googol",
)


def _format_not_finite(value):
    if math.isnan(value):
        return "NaN"
    if math.isinf(value) and value < 0:
        return "-Inf"
    if math.isinf(value) and value > 0:
        return "+Inf"
    return ""


def intword(value, format="%.1f"):
    try:
        if not math.isfinite(float(value)):
            return _format_not_finite(float(value))
        value = int(value)
    except (TypeError, ValueError):
        return str(value)

    if value < 0:
        value *= -1
        negative_prefix = "-"
    else:
        negative_prefix = ""

    if value < powers[0]:
        return f"{negative_prefix}{value}"

    ordinal = bisect.bisect_right(powers, value)
    largest_ordinal = ordinal == len(powers)

    ordinal -= 1
    power = powers[ordinal]
    chopped = value / power
    rounded_value = float(format % chopped)

    if not largest_ordinal and rounded_value == powers[ordinal + 1]:
        ordinal += 1
        rounded_value = 1.0

    unit = human_powers[ordinal]
    number = format % rounded_value
    return f"{negative_prefix}{number} {unit}"
```
