## Analysis

The issue: `validate('11144477735')` must return `'11144477735'`, but currently raises `InvalidChecksum`.

By tracing `_calc_check_digits('11144477735')`:
- `d1 = sum((10-i)*int(number[i]) for i in range(9))` sums digits 1,1,1,4,4,4,7,7,7 weighted 10..2 → then `d1 = (11 - d1) % 11 % 10`.
- For `11144477735`, the first check digit is `3`, the second `5`.
- The issue states both check digits are correct and the expected return is the compact number `'11144477735'`.

We only assert the behaviour the issue states: valid input returns the compact number. Test must fail now with `InvalidChecksum`, pass after fix.

We also include one closely related valid case could be avoided since the issue only states this one; to be safe we only assert the given example plus its formatted form (issue shows `111.444.777-35`), both reducing to the same compact value.

```python
import pytest

from alvo import validate, InvalidChecksum


def test_known_valid_cpf_returns_compact_number():
    assert validate('11144477735') == '11144477735'


def test_known_valid_cpf_formatted_returns_compact_number():
    assert validate('111.444.777-35') == '11144477735'


def test_known_valid_cpf_does_not_raise_invalid_checksum():
    try:
        result = validate('11144477735')
    except InvalidChecksum:
        pytest.fail("validate raised InvalidChecksum for a valid CPF")
    assert result == '11144477735'
```

---- revisão ----

Notes: All three assertions restate the issue's expected value `'11144477735'`; the formatted-input case is also given in the issue and reduces via `compact`. No memorized constants; all fail only due to the check-digit bug.

```python
import pytest

from alvo import validate, InvalidChecksum


def test_known_valid_cpf_returns_compact_number():
    assert validate('11144477735') == '11144477735'


def test_known_valid_cpf_formatted_returns_compact_number():
    assert validate('111.444.777-35') == '11144477735'


def test_known_valid_cpf_does_not_raise_invalid_checksum():
    try:
        result = validate('11144477735')
    except InvalidChecksum:
        pytest.fail("validate raised InvalidChecksum for a valid CPF")
    assert result == '11144477735'
```