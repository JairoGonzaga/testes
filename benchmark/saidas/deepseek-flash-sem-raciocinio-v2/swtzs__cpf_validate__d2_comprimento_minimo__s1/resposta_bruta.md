Analysis:
- The issue says any compacted CPF not exactly 11 digits must raise `InvalidLength`, but `validate` only checks `len(number) < 11`.
- So a 12-digit numeric string like `'111444777350'` (from the issue) passes the digit check, then fails the checksum comparison and raises `InvalidChecksum`.
- Expected value comes from the issue text: `validate('111444777350')` should raise `InvalidLength`.
- I'll also include a short CPF case (a few digits) to confirm the `< 11` branch still yields `InvalidLength`, which the source already shows.
- No exact checksum constants are needed; tests only assert exception types.

```python
import pytest

from alvo import validate, InvalidLength, InvalidChecksum


def test_too_many_digits_raises_invalid_length():
    with pytest.raises(InvalidLength):
        validate('111444777350')


def test_too_few_digits_raises_invalid_length():
    with pytest.raises(InvalidLength):
        validate('123')
```
```

---- revisão ----

Notes: Both assertions match the issue: `'111444777350'` (explicitly expected `InvalidLength`) fails now with `InvalidChecksum`; the `<11` case is traced from the source's existing `len(number) < 11` branch, so it's safe but not part of the reported bug's minimal fix, yet still valid.

```python
import pytest

from alvo import validate, InvalidLength


def test_too_many_digits_raises_invalid_length():
    with pytest.raises(InvalidLength):
        validate('111444777350')
```