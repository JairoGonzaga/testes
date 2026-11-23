**Explanation**

The `intword` function should translate the number `10**100` (a googol) into the human‑readable string **`'1.0 googol'`**.  
The current implementation mistakenly selects the previous suffix (“decillion”) because it uses `bisect_left` and then subtracts one from the returned index, so the test that checks for `'1.0 googol'` fails. After the bug is fixed (e.g., by handling an exact match correctly), the same test will pass.

**Test file (`test_issue.py`)**

```python
import pytest
from alvo import intword

def test_intword_googol():
    """
    A googol (10**100) must be rendered as '1.0 googol'.
    The current buggy implementation returns a decillion string,
    so this test fails until the issue is fixed.
    """
    assert intword(10**100) == "1.0 googol"
```

---- revisão ----

All assertions meet the requirements.  

```python
import pytest
from alvo import intword

def test_intword_googol():
    """
    A googol (10**100) must be rendered as '1.0 googol'.
    The current buggy implementation returns a decillion string,
    so this test fails until the issue is fixed.
    """
    assert intword(10**100) == "1.0 googol"
```