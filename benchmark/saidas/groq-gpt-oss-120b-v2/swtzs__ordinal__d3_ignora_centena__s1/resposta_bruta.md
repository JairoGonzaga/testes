**Analysis**  
The `ordinal` function should return the English ordinal representation of an integer.  
For numbers that end with 11, 12, or 13 the suffix must be `"th"` regardless of the last digit.  
The current implementation only checks `value in (11, 12, 13)`, so `ordinal(111)` incorrectly uses the `"st"` suffix and returns `"111st"`.  
The test asserts the correct result `"111th"` (and a control case for `11`). It will fail with the buggy code and pass after the fix.

```python
import pytest
from alvo import ordinal

def test_ordinal_111_returns_th():
    """Numbers ending with 11 should use the 'th' suffix."""
    assert ordinal(111) == "111th"

def test_ordinal_11_uses_th():
    """The special case 11 should also use the 'th' suffix."""
    assert ordinal(11) == "11th"
```

---- revisão ----

All assertions are directly supported by the issue description (111 → '111th') or by the existing code logic (11 → '11th').  

```python
import pytest
from alvo import ordinal

def test_ordinal_111_returns_th():
    """Numbers ending with 11 should use the 'th' suffix."""
    assert ordinal(111) == "111th"

def test_ordinal_11_uses_th():
    """The special case 11 should also use the 'th' suffix."""
    assert ordinal(11) == "11th"
```