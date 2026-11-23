Analysis:
The issue states that `naturalsize(3000000, binary=True)` should return `'2.9 MiB'` (since 3000000 / 1024^2 = 2.861), but the current code returns `'3.0 MiB'`. Tracing the code: `base = 1024 if gnu else 1000`. When `binary=True` and `gnu=False`, `base` is `1000`, so the value is divided by powers of 1000 instead of 1024. The expected value `2.9 MiB` comes from 3000000 / 1048576 = 2.861... formatted as "%.1f" → "2.9". I'll use the exact values from the issue.

```python
from alvo import naturalsize


def test_naturalsize_binary_uses_1024():
    # 3000000 / 1024**2 = 2.861... -> "2.9 MiB"
    assert naturalsize(3000000, binary=True) == "2.9 MiB"
```

---- revisão ----

Notes: The single assertion uses the exact value stated in the issue (`'2.9 MiB'` for 3000000). It fails now because the code divides by 1000 (giving `'3.0 MiB'`), and passes after the minimal fix `base = 1024 if gnu or binary else 1000` (3000000/1024**2 = 2.861 → `'2.9 MiB'`), so it fails solely due to the reported bug.

```python
from alvo import naturalsize


def test_naturalsize_binary_uses_1024():
    # 3000000 / 1024**2 = 2.861... -> "2.9 MiB"
    assert naturalsize(3000000, binary=True) == "2.9 MiB"
```