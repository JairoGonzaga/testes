Below is the source code of a Python module, `alvo.py`, and its test file, `test_alvo.py`, with the
LAST test function removed.

Write the missing last test function of this test file.
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


def test_c2_r1():
    # [R1/normal]
    assert apnumber(1) == 'one'


def test_c3_r1():
    # [R1/normal]
    assert apnumber(5) == 'five'


def test_c4_r1():
    # [R1/fronteira]
    assert apnumber(9) == 'nine'


def test_c5_r1():
    # [R1/normal]
    assert apnumber(2) == 'two'


def test_c6_r1():
    # [R1/normal]
    assert apnumber(3) == 'three'


def test_c7_r1():
    # [R1/normal]
    assert apnumber(4) == 'four'


def test_c8_r1():
    # [R1/normal]
    assert apnumber(6) == 'six'


def test_c9_r1():
    # [R1/normal]
    assert apnumber(7) == 'seven'


def test_c10_r1():
    # [R1/normal]
    assert apnumber(8) == 'eight'


def test_c11_r2():
    # [R2/fronteira]
    assert apnumber(10) == '10'


def test_c12_r2():
    # [R2/fronteira]
    assert apnumber(-1) == '-1'


def test_c13_r2():
    # [R2/normal]
    assert apnumber(100) == '100'


def test_c14_r3():
    # [R3/normal]
    assert apnumber('7') == 'seven'


def test_c15_r3():
    # [R3/normal]
    assert apnumber(3.9) == 'three'


def test_c16_r3():
    # [R3/normal]
    assert apnumber('10') == '10'


def test_c17_r4():
    # [R4/invalida]
    assert apnumber('foo') == 'foo'


def test_c18_r4():
    # [R4/invalida]
    assert apnumber(None) == 'None'


def test_c19_r4():
    # [R4/invalida]
    assert apnumber('3.9') == '3.9'


def test_c20_r5():
    # [R5/invalida]
    assert apnumber(float('inf')) == '+Inf'


def test_c21_r5():
    # [R5/invalida]
    assert apnumber(float('-inf')) == '-Inf'
```
