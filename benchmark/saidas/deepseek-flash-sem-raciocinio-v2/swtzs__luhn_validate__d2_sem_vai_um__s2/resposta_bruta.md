## Analysis

The Luhn checksum doubles digits in odd positions (from the right). When a doubled digit is >= 5, the standard algorithm subtracts 9 (i.e. `sum of digits`) — equivalent to `(i*2) % 9`, not `(i*2) % n` with `n = 10` (the alphabet length). The module uses `(i * 2) % n` where `n` is the **base** (10), not the digit-sum modulus (9). For `79927398713` (a standard valid Luhn number) the doubled digits include 5, 9, 6, etc. For example doubling 5 gives 10, whose digit sum is 1; `10 % 10 == 0`, which is wrong. Expected: `validate('79927398713')` returns `'79927398713'`.

The issue only states this concrete example and that it's valid. I'll test that example directly, plus a couple of standard valid Luhn numbers containing doubled digits >= 5 that the issue's framing ("some of the doubled digits are 5 or more") covers — but to stay safe I'll include only `79927398713` (given) and one other well-known valid Luhn string, `49927398716`, whose validity the issue's general claim implies. To be conservative, I'll stick to the single example the issue explicitly states as expected-output, since memorized constants are disallowed.

I'll assert: `validate('79927398713')` returns the same string (no exception raised).

```python
import pytest

from alvo import validate


def test_valid_luhn_number_with_high_doubled_digits():
    # Standard valid Luhn example from the issue: must not raise.
    assert validate("79927398713") == "79927398713"
```

---- revisão ----

Notes: The single assertion matches the issue's stated input/output exactly (`validate('79927398713')` returns the string); it fails now due to the `% n` vs digit-sum bug and passes after the minimal fix, and the expected value is copied from the task, not computed.

```python
from alvo import validate


def test_valid_luhn_number_with_high_doubled_digits():
    # Standard valid Luhn example from the issue: must not raise.
    assert validate("79927398713") == "79927398713"
```