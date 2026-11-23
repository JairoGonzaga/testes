**Explanation**

* `naturalsize(1)` is already correct – it returns `'1 Byte'`.
* The bug is that `naturalsize(-1)` falls through the special‑case check (`bytes_ == 1`) and uses the generic branch, producing `'-1 Bytes'` (plural).  
  The expected output, according to the issue, is `'-1 Byte'`.

The test below asserts the correct singular form for `-1`. It will fail with the current implementation and pass once the function is fixed. An additional sanity check confirms that the positive case still works.

```python
# test_issue.py
import pytest
from alvo import naturalsize

def test_negative_one_returns_singular_byte():
    # The bug: currently returns '-1 Bytes'
    assert naturalsize(-1) == '-1 Byte'

def test_positive_one_returns_singular_byte():
    # Control test – should already pass
    assert naturalsize(1) == '1 Byte'
```

---- revisão ----

All assertions are directly taken from the issue description and reflect the stated behavior.  

```python
# test_issue.py
import pytest
from alvo import naturalsize

def test_negative_one_returns_singular_byte():
    # Bug: currently returns '-1 Bytes', should be '-1 Byte'
    assert naturalsize(-1) == '-1 Byte'

def test_positive_one_returns_singular_byte():
    # Control: the positive case is already correct per the issue description
    assert naturalsize(1) == '1 Byte'
```