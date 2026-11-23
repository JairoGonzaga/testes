Analysis:
- The issue states `validate('79927398713')` must return `'79927398713'` (it's the standard valid Luhn example), currently raising `InvalidChecksum`.
- Standard Luhn: from the right, double every second digit; if a doubled value >= 10, subtract 9 (or sum its digits).
- The bug: the code computes `(i * 2) % n` with `n = 10`, i.e. `(i*2) % 10`, which subtracts 10 instead of 9 for digits >= 5 (e.g. 5*2=10 -> 0 instead of 1).
- Trace `79927398713`: doubled digits are 7,9,7,9,7 -> 14,18,14,18,14; correct reduction gives 5,9,5,9,5. The code gives 4,8,4,8,4, lowering the sum by 5, so `% 10 != 0` -> rejected.
- Expected value `'79927398713'` comes directly from the issue text.
- The fix is `(i*2) - n + 1` when `i*2 >= n` (equivalently `sum(divmod(i*2, n))`), so the test asserts only the documented return value.

```python
import pytest

from alvo import validate


def test_validate_standard_luhn_example():
    assert validate("79927398713") == "79927398713"
```

---- revisão ----

Notes: The single assertion matches the issue text exactly (input `'79927398713'`, expected return `'79927398713'`); it fails now due to the `(i*2) % n` bug and passes with the Luhn fix, and the unused `pytest` import is dropped.

```python
from alvo import validate


def test_validate_standard_luhn_example():
    assert validate("79927398713") == "79927398713"
```