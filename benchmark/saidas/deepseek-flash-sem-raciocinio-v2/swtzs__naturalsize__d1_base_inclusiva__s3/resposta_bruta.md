## Analysis

The bug: `naturalsize(1000)` returns `'1000 Bytes'` because of `abs_bytes <= base` — exactly `base` (1000) takes the byte branch, while it should move up to `kB`.

- `1000` should be `'1.0 kB'` (issue states this).
- The comparison should be strict (`<`), so values strictly below `base` stay in bytes.
- Expected values taken from the issue: `naturalsize(1000) == '1.0 kB'`.
- Closely related cases whose expected values follow directly from the issue's stated fix (exact multiples of the base convert, just-below stays in bytes): `naturalsize(1023)` stays `'1023 Bytes'`, `naturalsize(999)` stays `'999 Bytes'`, `naturalsize(1024*1024) == '1.0 MB'`, `naturalsize(1000*1000) == '1.0 MB'`.

```python
import pytest

from alvo import naturalsize


def test_exactly_one_kilobyte():
    # Issue: naturalsize(1000) must be '1.0 kB', not '1000 Bytes'
    assert naturalsize(1000) == "1.0 kB"


def test_below_kilobyte_stays_bytes():
    assert naturalsize(999) == "999 Bytes"


def test_just_below_binary_base_stays_bytes():
    assert naturalsize(1023) == "1023 Bytes"


def test_exactly_one_megabyte_decimal():
    assert naturalsize(1000 * 1000) == "1.0 MB"


def test_exactly_one_megabyte_binary():
    assert naturalsize(1024 * 1024) == "1.0 MB"
```

---- revisão ----

Notes: Only `1000 -> '1.0 kB'` is stated; `999`, `1023`, `1.0 MB` cases are unstated assumptions / code-dependent, so delete them and keep just the issue case.

```python
from alvo import naturalsize


def test_exactly_one_kilobyte():
    # Issue: naturalsize(1000) must be '1.0 kB', not '1000 Bytes'
    assert naturalsize(1000) == "1.0 kB"
```