Analysis:
The bug is in `apnumber`'s range check `if not 0 <= value < 9: return str(value)`.
This treats the valid single-digit range as 0-8, so `9` falls through and is returned as `'9'` instead of looking up `_APNUMBER_WORDS[9]` ('nine').
The issue explicitly states that single-digit numbers (0-9) should be spelled out, and gives the exact failing case `apnumber(9)` → should be `'nine'`. The `_APNUMBER_WORDS` tuple confirms indices 0..9 map to zero..nine.
Expected values are taken directly from the issue text and the tuple: `apnumber(9) == 'nine'`. A minimally related case, `apnumber(5) == 'five'`, is spelled out by the same mechanism; its value is read from the tuple, not computed.
The current code makes `apnumber(9)` return `'9'`, so the 9-test fails now and passes once the check is fixed to include 9; the 5-test passes both before and after, keeping the reproduction minimal without asserting unmentioned edge cases.

```python
from alvo import apnumber


def test_apnumber_nine_spelled_out():
    # Issue: apnumber(9) returned '9' instead of 'nine'.
    assert apnumber(9) == 'nine'


def test_apnumber_single_digit_still_spelled():
    # Closely related case, same mechanism, value from _APNUMBER_WORDS.
    assert apnumber(5) == 'five'
```

---- revisão ----

Notes:
- `apnumber(9) == 'nine'`: The task states 9 should be spelled out and explicitly gives 'nine'. Tracing: current check `not 0 <= 9 < 9` is True, so it returns `str(9)` -> `'9'` (FAILS now); after fix (allowing 9) it returns `_APNUMBER_WORDS[9]` = 'nine' (PASSES). Stated by task, value from task text. Keep.
- `apnumber(5) == 'five'`: Not stated in the task text; it's a real-world/generalization assumption. Tracing: `not 0 <= 5 < 9` is False, returns `_APNUMBER_WORDS[5]` = 'five' — passes on current code, so it does NOT reproduce the bug. Delete.

```python
from alvo import apnumber


def test_apnumber_nine_spelled_out():
    # Issue: apnumber(9) returned '9' instead of 'nine'.
    assert apnumber(9) == 'nine'
```