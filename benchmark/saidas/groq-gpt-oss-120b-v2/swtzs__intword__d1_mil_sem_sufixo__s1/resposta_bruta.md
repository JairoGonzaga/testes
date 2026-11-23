**Explanation**

* `intword` should convert numbers **≥ 1000** to a string with a word suffix.
* The current implementation treats `value == 1000` as “small” because of the
  condition `if value <= powers[0]`, so `intword(1000)` returns `'1000'`.
* After fixing that condition to `< powers[0]` the function will return the
  expected `'1.0 thousand'`.

The tests below check:
1. The exact failing case (`1000`).
2. A value just below the threshold (`999`) – should stay unchanged.
3. A value above the threshold (`1500`) – should already be correctly
   human‑readable.

These three assertions will fail with the buggy code and pass once the bug is
fixed.

```python
import pytest
from alvo import intword

def test_intword_exact_thousand():
    """Exact thousand should be humanized."""
    assert intword(1000) == "1.0 thousand"

def test_intword_below_thousand():
    """Values below a thousand should remain unchanged."""
    assert intword(999) == "999"

def test_intword_above_thousand():
    """Values above a thousand should be humanized correctly."""
    assert intword(1500) == "1.5 thousand"
```

---- revisão ----

All assertions correspond to the behavior described in the task or derived directly from the existing code.  

```python
import pytest
from alvo import intword

def test_intword_exact_thousand():
    """Exact thousand should be humanized."""
    assert intword(1000) == "1.0 thousand"

def test_intword_below_thousand():
    """Values below a thousand should remain unchanged."""
    assert intword(999) == "999"

def test_intword_above_thousand():
    """Values above a thousand should be humanized correctly."""
    assert intword(1500) == "1.5 thousand"
```