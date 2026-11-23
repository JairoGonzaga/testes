Analysis:
- The issue states `validate('')` currently returns `''` but should raise `InvalidFormat`.
- Tracing current code: `checksum('', "0123456789")` builds empty `values`, returns `0 % 10 == 0`, so `valid=True`, and `validate('')` returns `''`.
- The promised behaviour is only: empty string input raises `InvalidFormat`; it is not stated to return anything.
- The expected value (`InvalidFormat`) comes directly from the issue text.
- No other expected constants need to be computed; we only assert the empty-string case (plus keep it minimal).

```python
import pytest

from alvo import InvalidFormat, validate


def test_validate_empty_string_raises_invalid_format():
    with pytest.raises(InvalidFormat):
        validate('')
```

---- revisão ----

Notes: The single assertion matches the issue exactly — empty string should raise `InvalidFormat`; it fails now (current code returns `''`) and passes after the minimal fix, with the expected value taken directly from the issue text.

```python
import pytest

from alvo import InvalidFormat, validate


def test_validate_empty_string_raises_invalid_format():
    with pytest.raises(InvalidFormat):
        validate('')
```