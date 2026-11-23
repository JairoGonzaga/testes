Analysis:
- `validate('79927398713')` should return the input string; the issue states this number has a valid Luhn check digit.
- The bug is in `checksum`: it doubles `values[::2]` (rightmost digits first) instead of the digits at odd positions from the right (`values[1::2]`), so the sum isn't the standard Luhn sum.
- Expected value `'79927398713'` comes directly from the issue text (return value of `validate`).
- The test only needs to call `validate` with the issue's example and assert the returned string, plus assert no exception is raised.
- On current code `checksum` returns non-zero → `InvalidChecksum` raised → test fails; after fix it returns 0 → test passes.

```python
import pytest

from alvo import validate, checksum


def test_validate_accepts_textbook_luhn_number():
    # Issue: 79927398713 has a valid Luhn check digit and must be accepted.
    assert validate("79927398713") == "79927398713"


def test_checksum_of_textbook_luhn_number_is_zero():
    assert checksum("79927398713") == 0
```

---- revisão ----

Notes: The `checksum(...) == 0` assertion is not stated by the issue (it's inferred/algo-specific); keep only the `validate` return assertion stated in the issue.

```python
from alvo import validate


def test_validate_accepts_textbook_luhn_number():
    # Issue states: 79927398713 has a valid Luhn check digit.
    # Expected: validate returns '79927398713'.
    assert validate("79927398713") == "79927398713"
```