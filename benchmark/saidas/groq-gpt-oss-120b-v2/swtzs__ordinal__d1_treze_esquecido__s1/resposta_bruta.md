**Explanation**

The `ordinal` function should return the English ordinal suffix.  
According to the specification, the numbers 11, 12 and 13 (and any number ending with those two‑digit patterns) must use the suffix **“th”**.  
The current implementation only checks for 11 and 12, so `ordinal(13)` (and `ordinal(113)`, etc.) incorrectly returns “…rd”.

The test suite:

* verifies correct results for typical cases (`1st`, `2nd`, `3rd`, `21st`, …)  
* checks the special “teens” (`11th`, `12th`, `13th`, `111th`, `112th`, `113th`) – the failing ones are `13` and `113`  
* also confirms the handling of non‑finite values, which is already correct.

When the bug is fixed (by also treating `13` as a “teen”), all tests will pass.

```python
import pytest
from alvo import ordinal


@pytest.mark.parametrize(
    "value,expected",
    [
        (1, "1st"),
        (2, "2nd"),
        (3, "3rd"),
        (11, "11th"),
        (12, "12th"),
        (13, "13th"),   # bug: currently returns "13rd"
        (21, "21st"),
        (111, "111th"),
        (112, "112th"),
        (113, "113th"), # bug: currently returns "113rd"
    ],
)
def test_ordinal_suffixes(value, expected):
    """Ordinal numbers must use the correct suffix, especially the teens."""
    assert ordinal(value) == expected


def test_ordinal_non_finite():
    """Non‑finite numbers are handled by _format_not_finite."""
    assert ordinal(float("nan")) == "NaN"
    assert ordinal(float("inf")) == "+Inf"
    assert ordinal(float("-inf")) == "-Inf"
```

---- revisão ----

All assertions now correspond exactly to the behavior described in the issue (11, 12, 13 must end with “th”). No extra assumptions or unrelated cases are included.  

```python
import pytest
from alvo import ordinal


@pytest.mark.parametrize(
    "value,expected",
    [
        (11, "11th"),
        (12, "12th"),
        (13, "13th"),  # the bug: currently returns "13rd"
    ],
)
def test_ordinal_teens(value, expected):
    """11, 12 and 13 should always have the 'th' suffix."""
    assert ordinal(value) == expected
```