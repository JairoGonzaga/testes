**`test_issue.py`**

```python
import pytest
from alvo import ordinal

# --------------------------------------------------------------------------- #
# The original implementation incorrectly selects the suffix for 11, 12, 13
# by checking `value % 10` instead of the correct `value % 100`.  The tests
# below exercise the failing cases and confirm that the expected
# behaviour (using the “th” suffix for 11‑13, 111, etc.) is restored once
# the bug is fixed.
# --------------------------------------------------------------------------- #

def test_ordinal_11_returns_th():
    assert ordinal(11) == "11th"

def test_ordinal_12_returns_th():
    assert ordinal(12) == "12th"

def test_ordinal_13_returns_th():
    assert ordinal(13) == "13th"

def test_ordinal_111_returns_th():
    assert ordinal(111) == "111th"

# The following cases are correct in the current code but are added
# to demonstrate that the function handles common suffixes correctly.
def test_ordinal_1_returns_st():
    assert ordinal(1) == "1st"

def test_ordinal_2_returns_nd():
    assert ordinal(2) == "2nd"

def test_ordinal_3_returns_rd():
    assert ordinal(3) == "3rd"

def test_ordinal_4_returns_th():
    assert ordinal(4) == "4th"

# Non‑numeric values and special floats are handled by the helper
# functions; the tests verify that behaviour as well.
def test_ordinal_non_numeric():
    assert ordinal("abc") == "abc"

def test_ordinal_nan():
    assert ordinal(float("nan")) == "NaN"

def test_ordinal_pos_inf():
    assert ordinal(float("inf")) == "+Inf"

def test_ordinal_neg_inf():
    assert ordinal(float("-inf")) == "-Inf"
```

---- revisão ----

The only assertion needed is the one directly testing the bug described (ordinal(11)). All other checks were removed because they were not part of the task.  

```python
from alvo import ordinal

def test_ordinal_11_returns_th():
    assert ordinal(11) == "11th"
```