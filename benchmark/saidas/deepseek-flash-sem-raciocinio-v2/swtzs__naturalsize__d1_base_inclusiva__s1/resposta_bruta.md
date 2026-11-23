Analysis:
- Issue states `naturalsize(1000)` currently returns `'1000 Bytes'` and must return `'1.0 kB'`.
- From the code: base=1000, suffix=decimal ("kB",...). For value exactly equal to base, the `abs_bytes <= base` branch catches it and returns `'1000 Bytes'`.
- Expected `'1.0 kB'` comes from: exp=1, bytes_/1000 = 1.0, formatted with `"%.1f"` => `"1.0"`, space + suffix[0] => `"1.0 kB"`.
- The fix (not asked to implement) would change `<=` to `<`, so 1000 falls to exp computation. Test asserts the exact expected output string from the issue.

```python
import pytest
from alvo import naturalsize


def test_naturalsize_1000_bytes():
    assert naturalsize(1000) == "1.0 kB"
```

---- revisão ----

Notes: The single assertion matches the issue text exactly ('1.0 kB'), fails on current code due to the `<=` bug, and passes once changed to `<`.

```python
from alvo import naturalsize


def test_naturalsize_1000_bytes():
    assert naturalsize(1000) == "1.0 kB"
```