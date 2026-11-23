Analysis:
- The issue promises that `validate('')` raises `InvalidFormat`.
- Tracing current code: `checksum('')` → `str('')` is `''`; `reversed('')` is empty, so `values = ()`; sums are `0`; `0 % 10 == 0`, so `valid = True`; `validate` returns `''` instead of raising.
- Expected value comes directly from the issue: `InvalidFormat` must be raised for `''`.
- Only a couple of closely related cases are needed; the issue only states the empty-string case, so keep the test minimal and only assert `InvalidFormat` for `''`.

```python
import pytest

from alvo import validate, InvalidFormat


def test_validate_empty_string_raises_invalid_format():
    with pytest.raises(InvalidFormat):
        validate('')
```

---- revisão ----

The single assertion is directly stated by the issue (`validate('')` must raise `InvalidFormat`), fails on current code because `checksum('')` returns 0, and passes after a minimal fix that rejects empty input.

```python
import pytest

from alvo import validate, InvalidFormat


def test_validate_empty_string_raises_invalid_format():
    with pytest.raises(InvalidFormat):
        validate('')
```