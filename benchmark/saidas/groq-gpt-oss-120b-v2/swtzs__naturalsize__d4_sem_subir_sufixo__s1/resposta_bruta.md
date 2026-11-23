**Analysis**

The issue states that `naturalsize(999999)` should produce `'1.0 MB'` but currently returns `'1000.0 kB'`.  
The test will:

1. Call `naturalsize(999999)` and assert it equals `'1.0 MB'` (this fails now, passes after the fix).  
2. Include a sanity check for a value that is not affected by the bug (`999` bytes) to ensure normal behaviour remains unchanged.

**Test file (`test_issue.py`)**

```python
import pytest
from alvo import naturalsize

def test_naturalsize_just_before_megabyte():
    # The bug causes the unit not to be promoted when rounding up.
    # Expected result after the fix is '1.0 MB'.
    assert naturalsize(999_999) == "1.0 MB"

def test_naturalsize_regular_bytes():
    # Values below the base should remain unchanged.
    assert naturalsize(999) == "999 Bytes"
```

---- revisão ----

Notes: The extra sanity‑check assertion is not mentioned in the issue description, so it is removed. Only the assertion that directly reflects the reported bug remains.

```python
import pytest
from alvo import naturalsize

def test_naturalsize_just_before_megabyte():
    # The bug causes the unit not to be promoted when rounding up.
    # Expected result after the fix is '1.0 MB'.
    assert naturalsize(999_999) == "1.0 MB"
```