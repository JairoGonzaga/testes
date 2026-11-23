```python
from alvo import naturalsize


def test_naturalsize_exactly_one_kilobyte_is_converted():
    assert naturalsize(1000) == "1.0 kB"


def test_naturalsize_below_one_kilobyte_remains_bytes():
    assert naturalsize(999) == "999 Bytes"
```