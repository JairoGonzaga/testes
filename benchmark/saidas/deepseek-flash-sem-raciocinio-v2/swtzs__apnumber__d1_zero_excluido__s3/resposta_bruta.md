Analysis:
- Issue promises `apnumber(0)` returns `'zero'`; docs say numbers 0–9 are words.
- Current code has guard `if not 0 < value < 10: return str(value)`, which excludes 0 → returns `'0'`.
- Expected values `'zero'` and `'five'` come directly from the issue text and `_APNUMBER_WORDS`.
- Fix would change the guard to `0 <= value < 10`; tests must fail now and pass after.
- Also assert words list indexing stays correct for 1–9 (e.g. `'five'` for 5).

```python
import pytest

from alvo import apnumber


def test_apnumber_zero_is_word():
    # Issue: apnumber(0) should return 'zero', not '0'.
    assert apnumber(0) == "zero"


def test_apnumber_other_single_digits_still_work():
    # Issue states apnumber(5) -> 'five' works fine.
    assert apnumber(5) == "five"


def test_apnumber_one_is_word():
    assert apnumber(1) == "one"


def test_apnumber_nine_is_word():
    assert apnumber(9) == "nine"


def test_apnumber_ten_is_digit_string():
    # Outside 0..9, digits remain strings.
    assert apnumber(10) == "10"
```
</python>

---- revisão ----

Notes: `apnumber(1)`, `apnumber(9)`, and `apnumber(10)` expectations are not stated in the issue text (only 0 and 5 are), so I drop those extra tests; keep only the two issue-stated assertions.

```python
from alvo import apnumber


def test_apnumber_zero_is_word():
    # Issue: apnumber(0) should return 'zero', not '0'.
    assert apnumber(0) == "zero"


def test_apnumber_five_is_word():
    # Issue states apnumber(5) -> 'five' works fine.
    assert apnumber(5) == "five"
```
</python>