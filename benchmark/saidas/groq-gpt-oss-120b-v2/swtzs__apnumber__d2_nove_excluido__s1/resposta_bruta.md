**Analysis**

The function `apnumber` should return the word for any single‑digit integer from 0 to 9 inclusive.  
The current implementation only spells numbers where `0 <= value < 9`; therefore `apnumber(9)` falls through to the fallback `str(value)` and returns `'9'`.  

The test suite will:
1. Verify correct word output for a few valid single‑digit numbers (0, 5, 8).  
2. Check the problematic case `apnumber(9)` expecting `'nine'` – this assertion fails with the current code.  
3. Ensure numbers outside the single‑digit range (e.g., 10, ‑1) return their string representation, confirming that the fix must only affect the 0‑9 inclusive range.  
4. Confirm that non‑numeric input is returned unchanged.

```python
import pytest
from alvo import apnumber


def test_single_digit_numbers():
    # Correct word mapping for numbers inside the intended range
    assert apnumber(0) == "zero"
    assert apnumber(5) == "five"
    assert apnumber(8) == "eight"
    # The bug: 9 should be spelled out but currently returns "9"
    assert apnumber(9) == "nine"


def test_out_of_range_numbers():
    # Numbers not in 0‑9 should be returned as their string form
    assert apnumber(10) == "10"
    assert apnumber(-1) == "-1"


def test_non_numeric_input():
    # Non‑numeric values are returned unchanged as strings
    assert apnumber("abc") == "abc"
    # Also test a float that is not an integer but still finite
    assert apnumber(3.7) == "three"
```

---- revisão ----

All retained assertions are explicitly covered by the task (“single‑digit numbers should be spelled out”) and the expected words are taken directly from the module’s `_APNUMBER_WORDS` tuple. Removed tests that assert behavior not stated in the issue.  

```python
import pytest
from alvo import apnumber


def test_single_digit_numbers_spelled_out():
    # Numbers 0‑9 should be returned as words
    assert apnumber(0) == "zero"
    assert apnumber(5) == "five"
    assert apnumber(8) == "eight"
    # Bug: 9 should be spelled out but currently returns "9"
    assert apnumber(9) == "nine"
```