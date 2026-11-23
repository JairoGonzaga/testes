Analysis:
- The issue promises `naturalsize(1) == '1 Byte'` and `naturalsize(-1) == '-1 Byte'`.
- Current code only special-cases `bytes_ == 1`, so `-1` falls into `abs_bytes < base` and returns `'-1 Bytes'`.
- Expected values come directly from the issue text. The minimal fix extends the singular condition to `abs_bytes == 1`.
- Keep the test small: check `naturalsize(-1)` and the already-correct `naturalsize(1)`.

```python
from alvo import naturalsize


def test_naturalsize_negative_one_is_singular():
    assert naturalsize(-1) == "-1 Byte"


def test_naturalsize_one_is_singular():
    assert naturalsize(1) == "1 Byte"
```

---- revisão ----

Notes: Both expected values are copied directly from the issue; `naturalsize(-1) == '-1 Byte'` fails on current code only due to the reported bug and passes after extending the singular check to the absolute value; `naturalsize(1)` is the already-correct counterexample stated in the issue.

```python
from alvo import naturalsize


def test_naturalsize_negative_one_is_singular():
    assert naturalsize(-1) == "-1 Byte"


def test_naturalsize_one_is_singular():
    assert naturalsize(1) == "1 Byte"
```