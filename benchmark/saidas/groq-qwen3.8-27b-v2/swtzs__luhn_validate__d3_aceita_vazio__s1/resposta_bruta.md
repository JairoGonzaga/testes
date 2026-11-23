Analysis:
The issue states that `validate('')` should raise `InvalidFormat`, but currently returns `''`.
Tracing `checksum('')`:
- `str('')` is `''`
- `reversed('')` is an empty iterator
- `values` becomes `()`
- `sum(values[::2])` is `sum(())` which is `0`
- `sum(... for i in values[1::2])` is `0`
- Result is `(0 + 0) % 10` = `0`
- In `validate`, `valid` becomes `checksum('') == 0` which is `True`.
- So `validate('')` returns `''` instead of raising.
The fix would likely involve checking for empty strings in `validate` (or `checksum`) to raise `InvalidFormat`.
The test should assert that `validate('')` raises `InvalidFormat`.

```python
import pytest
from alvo import validate, InvalidFormat

def test_validate_empty_string_raises_invalid_format():
    with pytest.raises(InvalidFormat):
        validate('')
```

---- revisão ----

Notes: The single assertion directly matches the issue: `validate('')` should raise `InvalidFormat`. It fails on current code (returns `''`) and would pass after the minimal fix (checking for empty input and raising `InvalidFormat`). No other assertions are needed.

```python
import pytest
from alvo import validate, InvalidFormat

def test_validate_empty_string_raises_invalid_format():
    with pytest.raises(InvalidFormat):
        validate('')
```