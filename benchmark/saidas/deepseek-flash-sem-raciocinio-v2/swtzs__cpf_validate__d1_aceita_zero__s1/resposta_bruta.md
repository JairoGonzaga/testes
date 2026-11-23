Analysis:
- The issue states `validate('00000000000')` must raise `InvalidFormat`, and only this all-zeros case is mentioned.
- Current code: digits OK, length OK, and `_calc_check_digits('00000000000')` gives `'00'` matching the last two chars, so no error is raised.
- Expected: `InvalidFormat` is raised for the all-zeros CPF.
- I'll also assert that a normal valid CPF still works, and that `InvalidFormat` is a `ValueError`-family exception per the class hierarchy (both stated by source/issue).
- InvalidFormat is a subclass of ValidationError (ValueError), so pytest.raises(InvalidFormat) is the direct check.

```python
import pytest

from alvo import validate, InvalidFormat


def test_all_zeros_cpf_is_rejected():
    with pytest.raises(InvalidFormat):
        validate('00000000000')


def test_all_zeros_cpf_raises_invalid_format_not_checksum():
    # The issue says InvalidFormat specifically.
    try:
        validate('00000000000')
    except InvalidFormat:
        pass
    else:
        pytest.fail("validate('00000000000') did not raise InvalidFormat")
```
```

---- revisão ----

1. Both tests check only the stated behaviour: `validate('00000000000')` raising `InvalidFormat`. They fail on current code (accepted) and pass after fix. The second test is redundant but harmless; I'll keep just the clean pytest.raises test.

```python
import pytest

from alvo import validate, InvalidFormat


def test_all_zeros_cpf_is_rejected():
    with pytest.raises(InvalidFormat):
        validate('00000000000')
```