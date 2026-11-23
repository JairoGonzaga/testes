Analysis:
- Issue promises: `validate('')` must raise `InvalidFormat`.
- Current code: `checksum('')` returns `0` (empty sum % n == 0), so `valid` is True and `validate` returns `''`.
- Expected value: `InvalidFormat` exception type, explicitly stated in the issue.
- Only need to assert `InvalidFormat` is raised for empty string.

```python
import pytest

from alvo import validate, InvalidFormat


def test_validate_empty_string_raises_invalid_format():
    with pytest.raises(InvalidFormat):
        validate('')
```

---- revisão ----

The single assertion matches the issue exactly: `validate('')` must raise `InvalidFormat`. It fails now (returns `''`) and passes after a minimal fix (reject empty input). No changes needed.

```python
import pytest

from alvo import validate, InvalidFormat


def test_validate_empty_string_raises_invalid_format():
    with pytest.raises(InvalidFormat):
        validate('')
```