```python
from alvo import naturalsize


def test_naturalsize_exactly_one_kilobyte_is_converted():
    assert naturalsize(1000) == "1.0 kB"


def test_naturalsize_negative_exactly_one_kilobyte_is_converted():
    assert naturalsize(-1000) == "-1.0 kB"
```