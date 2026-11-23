Analysis:
- `naturalsize(1)` must return `'1 Byte'` (singular), as the issue states is correct.
- `naturalsize(-1)` must return `'-1 Byte'` (singular), per the issue's expected value.
- The current code only special-cases `bytes_ == 1`, so `-1` falls through to the `< base` branch which uses `"%d Bytes"`, giving `'-1 Bytes'`.
- The fix (per the issue) is to treat `-1` like `1` — singular. So the test just checks these exact strings.
- Derived expected values come directly from the issue text.

```python
from alvo import naturalsize


def test_naturalsize_one_byte_is_singular():
    assert naturalsize(1) == "1 Byte"


def test_naturalsize_negative_one_byte_is_singular():
    assert naturalsize(-1) == "-1 Byte"
```

---- revisão ----

Notes: Both assertions match the issue text exactly; `naturalsize(1) == '1 Byte'` is stated as correct and passes now, and `naturalsize(-1) == '-1 Byte'` is the stated expected output that fails now (returns `'-1 Bytes'`) and passes after treating `-1` as singular.

```python
from alvo import naturalsize


def test_naturalsize_one_byte_is_singular():
    assert naturalsize(1) == "1 Byte"


def test_naturalsize_negative_one_byte_is_singular():
    assert naturalsize(-1) == "-1 Byte"
```