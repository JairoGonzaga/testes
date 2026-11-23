**Analysis**

- The documentation states that `apnumber` should return word forms for numbers 0‑9.
- The current implementation returns the digit string for 0 because the range check is `0 < value < 10`.
- Therefore `apnumber(0)` currently yields `'0'` and the test `assert apnumber(0) == 'zero'` will fail.
- After fixing the range check to include zero (e.g., `0 <= value < 10`), the test will pass.
- We also include a sanity check that a typical non‑zero single digit (e.g., 5) already returns the correct word, ensuring the fix does not break existing behaviour.

```python
import pytest
from alvo import apnumber


def test_zero_is_spelled_out():
    """Zero should be returned as the word 'zero'."""
    assert apnumber(0) == "zero"


def test_other_single_digit_behaviour_unchanged():
    """Other single‑digit numbers should still be spelled out."""
    assert apnumber(5) == "five"
```

---- revisão ----

All assertions are directly supported by the issue description and use the expected values quoted there.

```python
import pytest
from alvo import apnumber


def test_zero_is_spelled_out():
    """Zero should be returned as the word 'zero'."""
    assert apnumber(0) == "zero"


def test_other_single_digit_behaviour_unchanged():
    """Other single‑digit numbers should still be spelled out."""
    assert apnumber(5) == "five"
```