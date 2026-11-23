Analysis:
- The issue promises `validate('79927398713')` returns `'79927398713'` (standard valid Luhn).
- The bug: `(i * 2) % n` doesn't sum digits when the doubled value ≥ 10; standard Luhn requires subtracting 9 (for decimal).
- For `79927398713`: doubled positions (from right) are 1,7,9,7,7→2,14,18,14,14; digit-sums: 2,5,9,5,5 sum=26; undoubled 3+8+2+9+7=29; total 55, 55%10=0 → valid.
- Expected value comes directly from the issue text (return the input).
- Also test a couple of closely related valid numbers stated by standard Luhn only via the same example's method — keep minimal: use only the issue example plus `checksum` consistency? To be safe, assert only the issue's example and that it doesn't raise.

```python
import pytest

from alvo import validate


def test_validate_standard_luhn_example():
    assert validate('79927398713') == '79927398713'
```

---- revisão ----

Notes: The single assertion matches the issue exactly (`validate('79927398713')` returns the input); expected value is copied from the issue text; it fails now due to the reported doubled-digit bug and passes with the minimal Luhn fix.

```python
import pytest

from alvo import validate


def test_validate_standard_luhn_example():
    assert validate('79927398713') == '79927398713'
```