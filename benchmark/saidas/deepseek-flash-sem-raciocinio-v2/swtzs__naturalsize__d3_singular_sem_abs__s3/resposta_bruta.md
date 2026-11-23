Analysis:
- The issue states `naturalsize(-1)` must return `'-1 Byte'`, and `naturalsize(1)` already returns `'1 Byte'`.
- In the source, the single-byte special case is `bytes_ == 1`, which excludes negatives like `-1`.
- The `< base` branch returns `"%d Bytes"` for `-1`, producing `'-1 Bytes'`.
- The fix (per the issue) is to treat the absolute single-byte case as singular too, so `-1` yields `'-1 Byte'`.
- Expected values come directly from the issue text: `'-1 Byte'` and the already-correct `'1 Byte'`.

```python
import pytest

from alvo import naturalsize


def test_naturalsize_positive_one_byte():
    assert naturalsize(1) == "1 Byte"


def test_naturalsize_negative_one_byte():
    assert naturalsize(-1) == "-1 Byte"


def test_naturalsize_negative_one_byte_is_not_plural():
    assert naturalsize(-1) != "-1 Bytes"
```

---- revisão ----

Notes: All three assertions match the issue text; `naturalsize(1) == "1 Byte"` is stated, `naturalsize(-1) == "-1 Byte"` is the required fix, and the `!= "-1 Bytes"` check restates the same bug output. Keeping all three is fine, though the third is redundant.

```python
from alvo import naturalsize


def test_naturalsize_positive_one_byte():
    assert naturalsize(1) == "1 Byte"


def test_naturalsize_negative_one_byte():
    assert naturalsize(-1) == "-1 Byte"


def test_naturalsize_negative_one_byte_is_not_plural():
    assert naturalsize(-1) != "-1 Bytes"
```