Analysis:
- Promised behaviour: with `binary=True`, sizes must be divided by powers of **1024**, not 1000.
- The issue states `naturalsize(3000000, binary=True)` must be `'2.9 MiB'` because 3000000 / 1024**2 = 2.86...
- Current code sets `base = 1024 if gnu else 1000`, so binary mode wrongly uses 1000.
- Test asserts the exact string from the issue: `'2.9 MiB'`.
- A closely related case from the same stated semantics: binary suffix with 1024 base. We only assert what the issue explicitly gives, to stay focused.

```python
import pytest

from alvo import naturalsize


def test_naturalsize_binary_uses_powers_of_1024():
    # From the issue: 3000000 / 1024**2 = 2.86..., formatted as '2.9' with 'MiB'.
    assert naturalsize(3000000, binary=True) == "2.9 MiB"
```

---- revisão ----

Notes: assertion is exactly the issue's stated expected value `'2.9 MiB'`; it fails now (base 1000 gives `'3.0 MiB'`) and passes after the minimal fix (base 1024 for binary), so keep it.

```python
from alvo import naturalsize


def test_naturalsize_binary_uses_powers_of_1024():
    # From the issue: 3000000 / 1024**2 = 2.86..., formatted as '2.9' with 'MiB'.
    assert naturalsize(3000000, binary=True) == "2.9 MiB"
```