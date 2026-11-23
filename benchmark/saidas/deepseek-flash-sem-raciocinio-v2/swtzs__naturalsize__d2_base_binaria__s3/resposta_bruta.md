Analysis:
- The issue promises `naturalsize(3000000, binary=True)` returns a value computed with base 1024, i.e. `3000000 / 1024**2 = 2.86` → formatted `%.1f` → `'2.9 MiB'`.
- The current code sets `base = 1024 if gnu else 1000`, so `binary=True` still uses 1000 → `'3.0 MiB'`.
- After the minimal fix (`base = 1024 if (gnu or binary) else 1000`), the same call yields `'2.9 MiB'`.
- Expected value `'2.9 MiB'` is stated directly in the issue text.
- I'll also test a plain `binary=True` value from the issue only; keep it minimal.

```python
from alvo import naturalsize


def test_naturalsize_binary_uses_1024():
    # From issue: 3000000 / 1024**2 = 2.86... -> '2.9 MiB'
    assert naturalsize(3000000, binary=True) == "2.9 MiB"
```

---- revisão ----

Notes: The single assertion matches the issue text exactly; `'2.9 MiB'` is stated in the issue; it fails now (returns `'3.0 MiB'`) and passes with the minimal base fix.

```python
from alvo import naturalsize


def test_naturalsize_binary_uses_1024():
    # From issue: 3000000 / 1024**2 = 2.86... -> '2.9 MiB'
    assert naturalsize(3000000, binary=True) == "2.9 MiB"
```