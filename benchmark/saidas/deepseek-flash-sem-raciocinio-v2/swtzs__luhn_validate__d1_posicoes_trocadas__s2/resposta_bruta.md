Analysis:
- `checksum` computes digits reversed, doubles every second digit starting from the rightmost (index 0 in `values[::2]`), sums `divmod(i*2, n)` for doubled digits and adds odd-index (non-doubled) digits, mod n.
- For `'79927398713'` (the textbook valid Luhn number), the expected result is `0` → `validate` should return the input `'79927398713'`.
- The issue states that `'79927398713'` has a valid check digit; expected value is the input string itself, per the task text.
- The bug: index parity is swapped — it should double digits at odd indexes (from the right), not even ones. So the current code returns a nonzero checksum and raises `InvalidChecksum`.
- Test asserts `validate('79927398713') == '79927398713'`; on current code this raises `InvalidChecksum`, so the test fails; after fixing parity it passes.

```python
import pytest

from alvo import validate


def test_textbook_luhn_number_is_valid():
    assert validate('79927398713') == '79927398713'
```

---- revisão ----

Notes: The single assertion is exactly the issue's stated expected behaviour (validate('79927398713') returns the input); it fails now with InvalidChecksum and passes after the parity fix, and the expected value is copied directly from the task text. Keep as is.

```python
import pytest

from alvo import validate


def test_textbook_luhn_number_is_valid():
    assert validate('79927398713') == '79927398713'
```