**Explanation**

The test suite checks three behaviours that are part of the public contract of `ordinal`:

1. Numeric values should be converted to the correct ordinal string – this is already
   correct in the current implementation.
2. Non‑numeric values that cannot be parsed as a number must be returned unchanged
   as a string.  The current implementation mistakenly returns an empty string,
   so the test will fail.
3. Values that are numeric but non‑finite (NaN or Inf) are handled by
   `_format_not_finite`; this is tested to guarantee that the function still
   works for those cases after the fix.

By asserting the exact expected output for each scenario the test will fail
before the bug is fixed and pass after the change that replaces the empty string
with `str(value)` in the `except` block. The test uses only the behaviour
explicitly stated in the issue and the source code.

```python
# test_issue.py
import pytest

from alvo import ordinal


def test_numeric_ordinals():
    """Numeric values should return correct ordinal strings."""
    assert ordinal(1) == "1st"
    assert ordinal(2) == "2nd"
    assert ordinal(3) == "3rd"
    assert ordinal(4) == "4th"
    assert ordinal(11) == "11th"
    assert ordinal(12) == "12th"
    assert ordinal(13) == "13th"
    assert ordinal(21) == "21st"
    assert ordinal(22) == "22nd"
    assert ordinal(23) == "23rd"
    assert ordinal(24) == "24th"


def test_non_numeric_returns_string():
    """Non‑numeric input should be returned as the string representation of the value."""
    # The current buggy implementation returns an empty string for this input.
    assert ordinal("something else") == "something else"
    # Other non‑numeric types should also be preserved.
    assert ordinal(["a", "list"]) == str(["a", "list"])
    assert ordinal(3.14) == "3.14"  # float that is not an int


def test_non_finite_values():
    """Non‑finite numeric values are delegated to _format_not_finite."""
    assert ordinal(float("nan")) == "NaN"
    assert ordinal(float("inf")) == "+Inf"
    assert ordinal(float("-inf")) == "-Inf"
```

---- revisão ----

**Notes:** Removed non‑numeric assertions that were not part of the issue statement (list and float). The remaining tests cover the promised behaviour and fail only because of the reported bug.  

```python
# test_issue.py
import pytest

from alvo import ordinal


def test_numeric_ordinals():
    """Numeric values should return correct ordinal strings."""
    assert ordinal(1) == "1st"
    assert ordinal(2) == "2nd"
    assert ordinal(3) == "3rd"
    assert ordinal(4) == "4th"
    assert ordinal(11) == "11th"
    assert ordinal(12) == "12th"
    assert ordinal(13) == "13th"
    assert ordinal(21) == "21st"
    assert ordinal(22) == "22nd"
    assert ordinal(23) == "23rd"
    assert ordinal(24) == "24th"


def test_non_numeric_returns_string():
    """Non‑numeric input should be returned as the string representation of the value."""
    # The current buggy implementation returns an empty string for this input.
    assert ordinal("something else") == "something else"


def test_non_finite_values():
    """Non‑finite numeric values are delegated to _format_not_finite."""
    assert ordinal(float("nan")) == "NaN"
    assert ordinal(float("inf")) == "+Inf"
    assert ordinal(float("-inf")) == "-Inf"
```