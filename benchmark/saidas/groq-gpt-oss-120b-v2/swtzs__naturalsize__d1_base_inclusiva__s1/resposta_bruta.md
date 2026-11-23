**Explanation**

* `naturalsize` is supposed to switch to the next unit when the absolute value is **greater than** the base (1000 for decimal).  
* The current implementation uses `<= base`, so `naturalsize(1000)` returns `"1000 Bytes"` instead of the expected `"1.0 kB"`.  
* The test checks the problematic call (`1000`) and also a value that should stay in the *Bytes* unit (`999`).  
* With the bug present the first assertion fails; after fixing the `<=` to `<` the test passes.

```python
# test_issue.py
import pytest
from alvo import naturalsize

def test_naturalsize_converts_exact_kilobyte():
    # The bug makes this return "1000 Bytes"; the correct output is "1.0 kB".
    assert naturalsize(1000) == "1.0 kB"

def test_naturalsize_below_threshold_stays_bytes():
    # Values strictly below the base must remain in the Bytes unit.
    assert naturalsize(999) == "999 Bytes"
```

---- revisão ----

Only the assertion that directly checks the reported bug is kept; the extra case is removed.  

```python
# test_issue.py
import pytest
from alvo import naturalsize

def test_naturalsize_converts_exact_kilobyte():
    # The bug makes this return "1000 Bytes"; the correct output is "1.0 kB".
    assert naturalsize(1000) == "1.0 kB"
```