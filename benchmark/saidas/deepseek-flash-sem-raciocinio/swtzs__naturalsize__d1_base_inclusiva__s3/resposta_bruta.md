```python
import pytest

from alvo import naturalsize


def test_naturalsize_exactly_one_kilobyte():
    assert naturalsize(1000) == "1.0 kB"


def test_naturalsize_negative_one_kilobyte():
    assert naturalsize(-1000) == "-1.0 kB"


def test_naturalsize_one_megabyte():
    assert naturalsize(1000**2) == "1.0 MB"


def test_naturalsize_just_below_one_kilobyte_still_bytes():
    assert naturalsize(999) == "999 Bytes"


def test_naturalsize_binary_one_kibibyte():
    assert naturalsize(1024, binary=True) == "1.0 KiB"
```