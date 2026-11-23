Below is the source code of a Python module, `alvo.py`, and the beginning of its test file,
`test_alvo.py` (imports and the first test function).

Write the NEXT test function of this test file.
- It must pass on this code and test behaviour of the module.
- The answer is only the code of the new test function (plus any extra import it needs at the top).
  It will be appended to the end of the test file shown below.

## Source: alvo.py

```python
from math import log

suffixes = {
    "decimal": ("kB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB", "RB", "QB"),
    "binary": ("KiB", "MiB", "GiB", "TiB", "PiB", "EiB", "ZiB", "YiB", "RiB", "QiB"),
    "gnu": "KMGTPEZYRQ",
}


def naturalsize(value, binary=False, gnu=False, format="%.1f"):
    if gnu:
        suffix = suffixes["gnu"]
    elif binary:
        suffix = suffixes["binary"]
    else:
        suffix = suffixes["decimal"]

    base = 1024 if (gnu or binary) else 1000
    bytes_ = float(value)
    abs_bytes = abs(bytes_)

    if abs_bytes == 1 and not gnu:
        return "%d Byte" % int(bytes_)

    if abs_bytes < base:
        return f"{int(bytes_)}B" if gnu else "%d Bytes" % int(bytes_)

    exp = int(min(log(abs_bytes, base), len(suffix)))
    if exp < len(suffix) and abs(float(format % (abs_bytes / (base**exp)))) >= base:
        exp += 1
    space = "" if gnu else " "
    return format % (bytes_ / (base**exp)) + space + suffix[exp - 1]
```

## Test file: test_alvo.py (current content)

```python
"""Testes de naturalsize."""

import math

import pytest

from alvo import naturalsize


def test_c1_r1():
    # [R1/invalida]
    with pytest.raises(ValueError):
        naturalsize('abc')
```
