**Analysis**

The `ordinal` function should return the ordinal string for a number, using the suffix “th” for numbers ending in 11, 12, 13.  
The current implementation checks `value % 10` against (11, 12, 13), which can never be true, so numbers like 11, 111, 112, 113 get the wrong suffix (“st”, “nd”, “rd”).  
The test asserts the correct suffix for such values and also checks a few typical cases to ensure the function’s overall behaviour matches the specification.  
With the buggy code the test for 11 (and other teen‑ending numbers) fails; after fixing the condition to use `value % 100`, all assertions pass.

```python
import pytest
from alvo import ordinal


@pytest.mark.parametrize(
    "value,expected",
    [
        (1, "1st"),
        (2, "2nd"),
        (3, "3rd"),
        (4, "4th"),
        (11, "11th"),
        (12, "12th"),
        (13, "13th"),
        (21, "21st"),
        (22, "22nd"),
        (23, "23rd"),
        (24, "24th"),
        (111, "111th"),
        (112, "112th"),
        (113, "113th"),
        (101, "101st"),
        (102, "102nd"),
        (103, "103rd"),
        (110, "110th"),
    ],
)
def test_ordinal_suffixes(value, expected):
    """Ordinal should use the correct suffix, especially for teen endings."""
    assert ordinal(value) == expected
```

---- revisão ----

Only the behavior explicitly mentioned in the issue (ordinal 11 should be “11th”) is asserted.

```python
import pytest
from alvo import ordinal


def test_ordinal_11_returns_th():
    """The issue states that ordinal(11) must return '11th'."""
    assert ordinal(11) == "11th"
```