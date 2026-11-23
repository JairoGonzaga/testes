Analysis:
- `binary=True` must use base 1024 (issue: "should use powers of 1024").
- Expected `naturalsize(3000000, binary=True)` == `'2.9 MiB'`, taken from the issue text (`3000000 / 1024**2 = 2.86...` → format `%.1f` → 2.9).
- Current code sets `base = 1024 if gnu else 1000`, ignoring `binary`, so it uses 1000 and returns `'3.0 MiB'`.
- I'll also check the byte and below-base paths don't change for `binary=True` in an obvious way: e.g. `naturalsize(2048, binary=True)` → `'2.0 KiB'` (1024**1, `%.1f`).
- Keep small: one main assertion from the issue plus a couple of closely derived cases.

```python
from alvo import naturalsize


def test_naturalsize_binary_uses_1024_base():
    # 3000000 / 1024**2 = 2.861... -> "2.9 MiB" per the issue
    assert naturalsize(3000000, binary=True) == "2.9 MiB"


def test_naturalsize_binary_small_values():
    assert naturalsize(1024, binary=True) == "1.0 KiB"
    assert naturalsize(2048, binary=True) == "2.0 KiB"


def test_naturalsize_binary_suffix_selection():
    # 1024**3 bytes = 1.0 GiB
    assert naturalsize(1024 ** 3, binary=True) == "1.0 GiB"
```

---- revisão ----

Notes: Keep only the issue-stated case `naturalsize(3000000, binary=True) == '2.9 MiB'`; drop the KiB/GiB cases whose expected values I derived myself rather than from the task text.

```python
from alvo import naturalsize


def test_naturalsize_binary_uses_1024_base():
    # 3000000 / 1024**2 = 2.86..., expected '2.9 MiB' per the issue
    assert naturalsize(3000000, binary=True) == "2.9 MiB"
```