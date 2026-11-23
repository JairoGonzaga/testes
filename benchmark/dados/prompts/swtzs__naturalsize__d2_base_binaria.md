You are given an issue report for a small Python project and the full source of the module it
concerns, `alvo.py`.

Write a pytest test file that REPRODUCES the issue:
- the tests must FAIL on the current code (because of the bug described in the issue), and
- the tests must PASS once the issue is fixed.

Rules:
- Import from the module with `from alvo import ...`. The test file will be saved as
  `test_issue.py` in the same folder as `alvo.py`.
- Do not modify, copy or re-implement the module. Do not fix the bug.
- The answer is a single complete, runnable pytest file.

## Issue: naturalsize(binary=True) gives wrong values

With `binary=True` the result should use powers of 1024 (KiB, MiB...), but the numbers look like they are computed with powers of 1000:

```python
>>> from alvo import naturalsize
>>> naturalsize(3000000, binary=True)
'3.0 MiB'
```

3000000 / 1024**2 = 2.86..., so expected `'2.9 MiB'`.

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

    base = 1024 if gnu else 1000
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
