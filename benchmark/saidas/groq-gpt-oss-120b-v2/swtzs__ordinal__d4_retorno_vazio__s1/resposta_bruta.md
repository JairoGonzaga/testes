**Analysis**

The issue states that `ordinal()` should return the original string for any value that cannot be converted to an integer.  
Current implementation catches the conversion error and returns `''`.  
The test will assert that a non‑numeric input (e.g., `'something else'`) is returned unchanged, which fails now and passes after fixing the function to return `str(value)`.  
Additional checks confirm that normal numeric inputs still produce the correct ordinal strings.

```python
import pytest
from alvo import ordinal


def test_ordinal_non_numeric_returns_original():
    # Non‑numeric input should be returned unchanged.
    assert ordinal("something else") == "something else"


def test_ordinal_none_returns_string_representation():
    # None cannot be converted to int; the function should return "None".
    assert ordinal(None) == "None"


def test_ordinal_numeric_values():
    # Verify that normal numeric handling is still correct.
    assert ordinal(1) == "1st"
    assert ordinal(2) == "2nd"
    assert ordinal(3) == "3rd"
    assert ordinal(4) == "4th"
    # Edge cases for the teens (11, 12, 13) all use "th"
    assert ordinal(11) == "11th"
    assert ordinal(12) == "12th"
    assert ordinal(13) == "13th"
    # Larger numbers
    assert ordinal(21) == "21st"
    assert ordinal(112) == "112th"
```

---- revisão ----

All assertions now directly reflect the described bug and the code’s defined behavior.

```python
import pytest
from alvo import ordinal


def test_ordinal_non_numeric_returns_original():
    # Non‑numeric input should be returned unchanged.
    assert ordinal("something else") == "something else"


def test_ordinal_numeric_values():
    # Verify that normal numeric handling follows the implementation.
    assert ordinal(1) == "1st"
    assert ordinal(2) == "2nd"
    assert ordinal(3) == "3rd"
    assert ordinal(4) == "4th"
    # Edge cases for the teens (11, 12, 13) all use "th"
    assert ordinal(11) == "11th"
    assert ordinal(12) == "12th"
    assert ordinal(13) == "13th"
    # Larger numbers
    assert ordinal(21) == "21st"
    assert ordinal(112) == "112th"
```