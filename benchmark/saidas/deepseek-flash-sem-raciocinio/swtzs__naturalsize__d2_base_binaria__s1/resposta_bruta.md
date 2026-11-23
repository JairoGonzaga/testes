```python
from alvo import naturalsize


def test_naturalsize_binary_uses_1024_powers():
    assert naturalsize(3000000, binary=True) == "2.9 MiB"


def test_naturalsize_binary_expected_boundaries():
    assert naturalsize(1024, binary=True) == "1.0 KiB"
    assert naturalsize(1024 ** 2, binary=True) == "1.0 MiB"
    assert naturalsize(1024 ** 3, binary=True) == "1.0 GiB"
```