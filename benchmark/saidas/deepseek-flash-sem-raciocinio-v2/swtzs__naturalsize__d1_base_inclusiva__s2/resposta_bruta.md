Analysis:
- Issue states: `naturalsize(1000)` must return `'1.0 kB'` (decimal, default).
- Current code: `abs_bytes <= base` triggers the Bytes branch for 1000, so it returns `'1000 Bytes'`. That's the bug.
- The promised behaviour: exactly one kilobyte (1000 with base 1000) must convert to the next unit — `1.0 kB`.
- Expected value comes directly from the issue text. The format string `"%.1f"` gives `"1.0"`, suffix `kB`.
- Keep test small: reproduce the reported call and its exact expected output.

```python
from alvo import naturalsize


def test_naturalsize_1000_decimal():
    assert naturalsize(1000) == "1.0 kB"
```

---- revisão ----

Notes: single assertion matches the issue exactly (`naturalsize(1000)` → `'1.0 kB'`), fails now on the Bytes branch, passes after the minimal `<=` → `<` fix; no changes needed.

```python
from alvo import naturalsize


def test_naturalsize_1000_decimal():
    assert naturalsize(1000) == "1.0 kB"
```