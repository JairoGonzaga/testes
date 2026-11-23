### Analysis

The issue is that `intword(10**100)` returns a huge number with `'decillion'` instead of `'1.0 googol'`.

Tracing the code:
- `powers = [10**3, ..., 10**33, 10**100]`, so `powers[11] == 10**100`.
- `human_powers[11] == "googol"`.
- For `value = 10**100`, `bisect_left(powers, value)` returns `11` (index of googol).
- `ordinal = 11`, `largest_ordinal = (11 == 12)` → `False`.
- Then `ordinal -= 1` → `10`, `power = 10**33` (decillion).
- `chopped = 10**100 / 10**33` which overflows to a huge float.
- `rounded_value = float("%.1f" % chopped)` is a huge number.
- `powers[11] // power == 10**100 // 10**33` — this is a huge Python int, not equal to `rounded_value`.
- Result: huge number + `"decillion"`.

Expected: `'1.0 googol'`.

Test inputs/outputs come directly from the issue: `intword(10**100) == '1.0 googol'`. The `@pytest.mark.parametrize` includes a closely related case `10**101` should be `'10.0 googol'`? The issue doesn't state it, so I'll only assert `10**100`.

```python
import pytest

from alvo import intword


def test_intword_googol():
    assert intword(10**100) == '1.0 googol'
```

---- revisão ----

Only `'1.0 googol'` for `10**100` is stated by the issue; keep just that single assertion.

```python
from alvo import intword


def test_intword_googol():
    assert intword(10**100) == '1.0 googol'
```