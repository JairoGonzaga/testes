**Explanation of the test**

The `intword` function is supposed to convert a large integer into a human‑readable string using powers of ten.  
For `10**100` (a googol) the correct output, as described in the issue, is the string `'1.0 googol'`.  
The current implementation incorrectly formats this number as a gigantic `decillion` string because the
check that would promote the value to the next power uses a float comparison that fails when the number
cannot be represented exactly in binary floating‑point.

The test simply asserts that `intword(10**100)` equals `'1.0 googol'`.  
With the buggy code this assertion fails; after the fix it passes.

```python
# test_issue.py
import pytest
from alvo import intword

def test_googol_is_correctly_humanized():
    """
    intword(10**100) should return '1.0 googol'.
    With the current buggy implementation it returns a huge decillion string,
    so the test fails.  After the bug is fixed the test passes.
    """
    assert intword(10**100) == "1.0 googol"
```

---- revisão ----

The test confirms that `intword(10**100)` should return `'1.0 googol'` as specified in the issue, and will fail with the current buggy code but pass once the bug is fixed.

```python
# test_issue.py
import pytest
from alvo import intword

def test_googol_is_correctly_humanized():
    """
    intword(10**100) should return '1.0 googol'.
    With the current buggy implementation it returns a huge decillion string,
    so the test fails.  After the bug is fixed the test passes.
    """
    assert intword(10**100) == "1.0 googol"
```