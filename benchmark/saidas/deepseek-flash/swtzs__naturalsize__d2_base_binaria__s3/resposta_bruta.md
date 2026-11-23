```python
from alvo import naturalsize


def test_naturalsize_binary_mib_uses_1024():
    assert naturalsize(3_000_000, binary=True) == "2.9 MiB"


def test_naturalsize_binary_gib_uses_1024():
    assert naturalsize(2 * 1024**3, binary=True) == "2.0 GiB"


def test_naturalsize_binary_selects_kib_below_mib_threshold():
    assert naturalsize(1_000_000, binary=True) == "976.6 KiB"
```