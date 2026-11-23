## Analysis

- The issue promises `apnumber(9)` returns `'nine'` (spelled-out word for single-digit `9`).
- `_APNUMBER_WORDS` contains words index `0..9`, with `"nine"` at index 9.
- The module's guard `if not 0 <= value < 9` excludes 9, sending it to `str(value)` → `'9'`.
- Expected value `'nine'` comes from the issue statement and the word tuple.
- Also `apnumber(0)` → `'zero'` (in range, tuple[0]) as a sanity check that the words list is used.
- Test must fail now (`'9'`) and pass after widening the bound to include 9.

```python
from alvo import apnumber


def test_apnumber_nine_is_spelled_out():
    # Issue: apnumber(9) must be 'nine', not '9'.
    assert apnumber(9) == "nine"


def test_apnumber_zero_is_spelled_out():
    # Sanity: in-range single digit still uses the word table.
    assert apnumber(0) == "zero"
```

---- revisão ----

Notes: Both assertions hold — `apnumber(9) == "nine"` is stated in the issue (expected `'nine'`); `apnumber(0) == "zero"` is traced from code (`0 <= 0 < 9` true → `_APNUMBER_WORDS[0] == "zero"`), and the first fails on current code only due to the `< 9` bound. No changes needed.

```python
from alvo import apnumber


def test_apnumber_nine_is_spelled_out():
    # Issue: apnumber(9) must be 'nine', not '9'.
    assert apnumber(9) == "nine"


def test_apnumber_zero_is_spelled_out():
    # Sanity: in-range single digit still uses the word table.
    assert apnumber(0) == "zero"
```