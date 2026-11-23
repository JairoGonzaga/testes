**Analysis**

`intword` should keep a leading “‑” for negative numbers.  
The function currently clears `negative_prefix` for both branches, so:

* `intword(-1000000)` returns `'1.0 million'` instead of `'-1.0 million'`.
* `intword(-500)` returns `'500'` instead of `'-500'`.

The tests verify these two cases and also confirm that a positive value is unchanged, ensuring the fix only affects the sign handling.

```python
import pytest
from alvo import intword

def test_intword_negative_large_number():
    # Negative number that is formatted with a human‑readable unit
    result = intword(-1_000_000)
    assert result == "-1.0 million", "Negative sign should be preserved for large values"

def test_intword_negative_small_number():
    # Negative number that is below the first power threshold
    result = intword(-500)
    assert result == "-500", "Negative sign should be preserved for small values"

def test_intword_positive_number_unchanged():
    # Positive number should remain unchanged (sanity check)
    assert intword(500) == "500"
    assert intword(1_000_000) == "1.0 million"
```

---- revisão ----

The extra assertions for positive numbers and the small‑negative case are not required by the issue description, so they are removed. The remaining test checks exactly the behavior the issue talks about.

```python
import pytest
from alvo import intword

def test_intword_negative_large_number():
    # The issue states that the minus sign is dropped for negative numbers.
    # The correct output should preserve the sign.
    result = intword(-1_000_000)
    assert result == "-1.0 million"
```