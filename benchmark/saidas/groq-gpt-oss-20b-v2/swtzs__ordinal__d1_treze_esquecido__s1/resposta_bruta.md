```python
import pytest
from alvo import ordinal

# --------------------------------------------------------------------------- #
# What the tests check
# --------------------------------------------------------------------------- #
# 1. 13 should return '13th' (not '13rd')
# 2. 11 and 12 also end with 'th', not 'st'/'nd'
# 3. Normal rule for other numbers should still hold (e.g., 21 -> '21st')
# --------------------------------------------------------------------------- #

def test_ordinal_13():
    """13 must be suffixed with 'th', not 'rd'."""
    assert ordinal(13) == "13th"

def test_ordinal_11():
    """11 must be suffixed with 'th'."""
    assert ordinal(11) == "11th"

def test_ordinal_12():
    """12 must be suffixed with 'th'."""
    assert ordinal(12) == "12th"

def test_ordinal_regular_cases():
    """Other numbers use the usual English ordinal endings."""
    assert ordinal(21) == "21st"
    assert ordinal(22) == "22nd"
    assert ordinal(23) == "23rd"
    assert ordinal(24) == "24th"
```

---- revisão ----

**Notes:** All assertions reflect behavior explicitly described in the issue and the module code. The tests will fail only on the current buggy implementation (specifically for `ordinal(13)`) and pass once the minimal fix is applied.

```python
import pytest
from alvo import ordinal

# What the tests check
# 1. 13 must be suffixed with 'th', not 'rd'.
# 2. 11 and 12 also end with 'th'.
# 3. Normal rule for other numbers should still hold (e.g., 21 -> '21st').

def test_ordinal_13():
    """13 must be suffixed with 'th', not 'rd'."""
    assert ordinal(13) == "13th"

def test_ordinal_11():
    """11 must be suffixed with 'th'."""
    assert ordinal(11) == "11th"

def test_ordinal_12():
    """12 must be suffixed with 'th'."""
    assert ordinal(12) == "12th"

def test_ordinal_regular_cases():
    """Other numbers use the usual English ordinal endings."""
    assert ordinal(21) == "21st"
    assert ordinal(22) == "22nd"
    assert ordinal(23) == "23rd"
    assert ordinal(24) == "24th"
```