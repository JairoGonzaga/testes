The promised behaviour (per the issue and the docs echoed in it): `apnumber` should return English words for the single digits 0–9, e.g. `apnumber(5) -> 'five'` and `apnumber(0) -> 'zero'`.

Root cause in `alvo.py`: the guard `if not 0 < value < 10:` uses a strict lower bound, so `value == 0` fails the check and is returned as `'0'`. The fix is to make the condition `0 <= value < 10`.

Each expected value is stated directly by the issue: `apnumber(0)` must be `'zero'` (the bug), and `apnumber(5)` must be `'five'` (the working case the issue cites). I also add `apnumber(9) -> 'nine'` as a similarly stated endpoint to complete the covered single-digit range, all sourced from the task text (no mental constant computation). The test for `apnumber(0)` will fail on the current code and pass after the fix; the digit tests pass in both states as provided regression checks.

```python
from alvo import apnumber


def test_apnumber_zero_is_spelled_out():
    # Directly reproduces the reported bug: zero must be a word, not a digit string.
    assert apnumber(0) == "zero"


def test_apnumber_single_digits_are_spelled_out():
    # Working case cited in the issue (5 -> 'five'), plus the upper-endpoint nine.
    assert apnumber(5) == "five"
    assert apnumber(9) == "nine"
```

---- revisão ----

The only behavior stated by the task is `apnumber(0)` → `'zero'` (the bug) and `apnumber(5)` → `'five'` (the working case the issue cites). My `apnumber(9) == "nine"` assertion, while true after fixing the code, is not stated by the task text and risks a future change with a different single-digit table, so I delete it per the "when in doubt, delete" rule. I keep the zero assertion (reproduces the bug; fails now, passes after the `0 <= value` fix) and the five assertion (stated in the issue; passes in both states as a regression check).

```python
from alvo import apnumber


def test_apnumber_zero_is_spelled_out():
    # Directly reproduces the reported bug: zero must be a word, not a digit string.
    assert apnumber(0) == "zero"


def test_apnumber_single_digit_is_spelled_out():
    # Working case cited in the issue (5 -> 'five').
    assert apnumber(5) == "five"
```