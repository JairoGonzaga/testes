Analysis: The issue states that `validate('00000000000')` must raise `InvalidFormat`. Currently `_calc_check_digits('00000000000')` returns `'00'` which equals `number[-2:]`, so no error is raised. The expected behaviour (from the issue text) is that `InvalidFormat` is raised for an all-zeros CPF. Also verify a normal valid CPF still returns itself, using a value whose check digits we trace directly through `_calc_check_digits` (no memorized constants). To get a valid input, we can compute via the module's own public `_calc_check_digits`? That is private; instead trace: for a number like '11144477735' we'd need memorized check digits — avoid. Use the issue's stated outputs only: all-zeros must raise `InvalidFormat`. Additionally assert the exception type is exactly the `InvalidFormat` subclass semantics (i.e. `InvalidLength` is a subclass, but issue says InvalidFormat — use pytest.raises(InvalidFormat) which passes for subclasses; that's per issue).

```python
import pytest

from alvo import validate, InvalidFormat, _calc_check_digits


def _make_valid(base9):
    """Build a valid 11-digit CPF from 9 digits using the module's own algorithm."""
    return base9 + _calc_check_digits(base9 + "00")


def test_all_zeros_raises_invalid_format():
    with pytest.raises(InvalidFormat):
        validate("00000000000")


def test_all_zeros_with_punctuation_raises_invalid_format():
    with pytest.raises(InvalidFormat):
        validate("000.000.000-00")


def test_valid_number_still_accepted():
    # 9 leading digits with a non-trivial value; check digits computed by the module itself
    base = "123456789"
    number = base + _calc_check_digits(base + "00")
    assert validate(number) == number
```

---- revisão ----

Notes: `_make_valid` is unused/dead and the third test relies on internal `_calc_check_digits` plus an assumed "must still be accepted" behaviour not stated by the issue — delete it; keep only the all-zeros cases which are exactly what the issue promises.

```python
import pytest

from alvo import validate, InvalidFormat


def test_all_zeros_raises_invalid_format():
    with pytest.raises(InvalidFormat):
        validate("00000000000")


def test_all_zeros_with_punctuation_raises_invalid_format():
    with pytest.raises(InvalidFormat):
        validate("000.000.000-00")
```