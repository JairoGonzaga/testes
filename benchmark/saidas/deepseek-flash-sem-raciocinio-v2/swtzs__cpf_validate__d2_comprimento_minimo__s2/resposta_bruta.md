Analysis: The issue states that any compacted CPF whose digit string is not exactly 11 digits should raise `InvalidLength`, and shows `validate('111444777350')` (12 digits) currently raising `InvalidChecksum`. Expected value `InvalidLength` comes directly from the issue text. The bug is `len(number) < 11` in `validate`; it should require exactly 11, so 12-digit input reaches the length check and fails there before checksum computation.

```python
import pytest

from alvo import InvalidLength, validate


def test_cpf_with_12_digits_raises_invalid_length():
    with pytest.raises(InvalidLength):
        validate('111444777350')
```

---- revisão ----

Notes: The single assertion is exactly the issue's reported case; the expected `InvalidLength` is copied from the issue text, it fails now (raises `InvalidChecksum`) and would pass after the minimal fix to the length check. No changes needed.

```python
import pytest

from alvo import InvalidLength, validate


def test_cpf_with_12_digits_raises_invalid_length():
    with pytest.raises(InvalidLength):
        validate('111444777350')
```