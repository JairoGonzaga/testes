Analysis:
- The issue states: any CPF whose compacted form is not exactly 11 digits must raise `InvalidLength`.
- Currently, `validate` only raises `InvalidLength` when `len(number) < 11`; longer inputs fall through to the checksum check.
- `validate('111444777350')` compacts to `'111444777350'` (12 digits) and is all digits and > 0, so it reaches `_calc_check_digits` and raises `InvalidChecksum`.
- Expected behavior after fix: `InvalidLength` for the 12-digit input from the issue.
- I'll also test a longer input (e.g., the same digits + one more) expecting `InvalidLength`; the expected value is directly derived from the issue's rule ("not exactly 11 digits").
- Note `InvalidLength` subclasses `InvalidFormat` (which subclasses `ValidationError`/`ValueError`), so I'll assert on `InvalidLength` specifically to distinguish from `InvalidChecksum`.

```python
import pytest

from alvo import validate, InvalidLength, InvalidChecksum


def test_cpf_with_12_digits_raises_invalid_length():
    # From the issue: too many digits should be InvalidLength, not InvalidChecksum.
    with pytest.raises(InvalidLength):
        validate("111444777350")


def test_cpf_with_12_digits_does_not_raise_invalid_checksum():
    try:
        validate("111444777350")
    except InvalidChecksum:
        pytest.fail("validate raised InvalidChecksum instead of InvalidLength")
    except InvalidLength:
        pass
    else:
        pytest.fail("validate did not raise InvalidLength")


def test_cpf_with_13_digits_raises_invalid_length():
    # Any compacted form not exactly 11 digits should be InvalidLength.
    with pytest.raises(InvalidLength):
        validate("1114447773501")
```

---- revisão ----

Notes: All three tests rely on the issue's stated rule (exactly 11 digits → otherwise `InvalidLength`); the 13-digit case is a direct derived case of the same rule. The second test is redundant but harmless; I'll keep it simple by removing it and keeping the two clear cases.

```python
import pytest

from alvo import validate, InvalidLength


def test_cpf_with_12_digits_raises_invalid_length():
    # From the issue: too many digits should be InvalidLength, not InvalidChecksum.
    with pytest.raises(InvalidLength):
        validate("111444777350")


def test_cpf_with_13_digits_raises_invalid_length():
    # Any compacted form not exactly 11 digits should be InvalidLength.
    with pytest.raises(InvalidLength):
        validate("1114447773501")
```