```python
import pytest

from alvo import naturalsize


def test_one_kilobyte_decimal():
    assert naturalsize(1000) == "1.0 kB"


def test_one_kilobyte_binary():
    assert naturalsize(1024, binary=True) == "1.0 KiB"


def test_one_kilobyte_gnu():
    assert naturalsize(1024, gnu=True) == "1.0K"


def test_thousand_bytes_decimal():
    assert naturalsize(1000) == "1.0 kB"
    assert naturalsize(999) == "999 Bytes"
```