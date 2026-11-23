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

    if not largest_ordinal and rounded_value == powers[ordinal + 1] // power:
        ordinal += 1
        rounded_value = 1.0

    unit = human_powers[ordinal]
    number = format % rounded_value
    return f"{negative_prefix}{number} {unit}"
```
