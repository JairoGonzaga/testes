Let me trace the code. `validate('00000000000')`: `compact` → `'00000000000'`, `isdigits` true, length 11, `_calc_check_digits`: d1 = sum of zeros = 0 → `(11-0)%11%10` = `0%10` = 0; d2 = 0 + 2*0 = 0 → 0; returns `'00'` == last two chars `'00'` → no error, returns the number. The issue states it should raise `InvalidFormat`. Expected values come from the issue: `'00000000000'` → raises `InvalidFormat`.

```python
import pytest

from alvo import validate, InvalidFormat


def test_all_zeros_cpf_is_rejected():
    with pytest.raises(InvalidFormat):
        validate('00000000000')
```

---- revisão ----

Check: `validate('00000000000')` raises `InvalidFormat` — explicitly stated ("Expected: `InvalidFormat` is raised"), and `InvalidFormat` is exported from `alvo`. Trace confirms current code returns the number, so it fails now and passes with the minimal fix. No violations.

```python
import pytest

from alvo import validate, InvalidFormat


def test_all_zeros_cpf_is_rejected():
    with pytest.raises(InvalidFormat):
        validate('00000000000')
```