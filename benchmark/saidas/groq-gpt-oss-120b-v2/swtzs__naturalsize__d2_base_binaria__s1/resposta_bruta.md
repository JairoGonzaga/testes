**Analysis**

The `naturalsize` function should use a base of 1024 when `binary=True`, but the current code sets `base = 1024` only when `gnu` is true, otherwise it always uses 1000.  
Therefore `naturalsize(3_000_000, binary=True)` returns `'3.0 MiB'` (decimal calculation) instead of the correct `'2.9 MiB'` (binary calculation).  
The test asserts the correct binary output; it will fail now and pass after the bug is fixed.

```python
import pytest
from alvo import naturalsize

def test_naturalsize_binary_uses_1024():
    # 3_000_000 bytes / 1024**2 = 2.861… → rounded to one decimal place → "2.9 MiB"
    assert naturalsize(3_000_000, binary=True) == "2.9 MiB"
```

---- revisão ----

All checks passed – the single assertion matches the expected behavior described in the issue.  

```python
import pytest
from alvo import naturalsize

def test_naturalsize_binary_uses_1024():
    # According to the issue, 3,000,000 bytes with binary=True should be formatted as "2.9 MiB"
    assert naturalsize(3_000_000, binary=True) == "2.9 MiB"
```