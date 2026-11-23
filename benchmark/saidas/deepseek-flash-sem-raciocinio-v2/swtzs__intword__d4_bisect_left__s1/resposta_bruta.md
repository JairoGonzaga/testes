```python
from alvo import intword

def test_intword_googol():
    assert intword(10**100) == '1.0 googol'

def test_intword_googol_close():
    # Just above a googol still in the same bucket
    assert intword(10**100 + 1) == '1.0 googol'
```

**Analysis**

`intword(10**100)` should be `'1.0 googol'` per the issue. `powers` includes `10**100` and `human_powers` includes `"googol"`. Currently `bisect_left(powers, 10**100) == 11`, then `ordinal -= 1` gives 10 (decillion), so it computes `10**100 / 10**33` as a float — overflowing mantissa precision — and formats a huge decimal string with `decillion`. The fix should make the googol bucket be selected (`ordinal` = 11) so the output is `format % 1.0` = `'1.0'` and `human_powers[11]` = `'googol'`. Expected values come directly from the issue (`'1.0 googol'`); the `+1` case follows the same bucket since `10**100 + 1` still rounds to `1.0` relative to `10**100`.

---- revisão ----

Notes: Keep only the exact case stated in the issue (`'1.0 googol'`); delete the `+1` case since its expected value is my inference, not stated.

```python
from alvo import intword

def test_intword_googol():
    assert intword(10**100) == '1.0 googol'
```