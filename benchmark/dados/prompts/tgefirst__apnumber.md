Below is the source code of a Python module, `alvo.py`, and the beginning of its test file,
`test_alvo.py` (imports and the first test function).

Write the NEXT test function of this test file.
- It must pass on this code and test behaviour of the module.
- The answer is only the code of the new test function (plus any extra import it needs at the top).
  It will be appended to the end of the test file shown below.

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
    if not 0 <= value < 10:
        return str(value)
    return _APNUMBER_WORDS[value]
```

## Test file: test_alvo.py (current content)

```python
"""Testes de apnumber."""

import math

import pytest

from alvo import apnumber


def test_c1_r1():
    # [R1/fronteira]
    assert apnumber(0) == 'zero'
```
