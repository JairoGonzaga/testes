## Analysis

- The issue promises `intword(1000)` should return `'1.0 thousand'`.
- In `alvo.py`, `powers[0] == 10**3 == 1000`.
- The guard `if value <= powers[0]: return f"{negative_prefix}{value}"` returns `'1000'` for `value == 1000` (boundary is `<=`, should let 1000 fall through to the word-suffix path).
- After the fix, `value=1000` proceeds: `ordinal = bisect_right(powers, 1000) = 1`, `ordinal -= 1 → 0`, `power=1000`, `chopped = 1000/1000 = 1.0`, `format % chopped == "1.0"`, boundary check `(powers[1] // powers[0]) == 10**6 // 10**3 == 1000`, `rounded_value` is `1.0`, not equal → no ordinal bump. Unit `human_powers[0] == "thousand"`. Result `'1.0 thousand'`.
- Negative case: `intword(-1000)` → `'-1.0 thousand'` (negative_prefix prepended).
- Small values like `999` still return `'999'` (below power) — this stays correct.
- Tests target exactly the reported condition: 1000 → `'1.0 thousand'`, plus the symmetric negative case which the same code path produces.

```python
import pytest

from alvo import intword


def test_intword_1000_is_humanized():
    assert intword(1000) == "1.0 thousand"


def test_intword_negative_1000_is_humanized():
    assert intword(-1000) == "-1.0 thousand"


def test_intword_below_power_is_unchanged():
    # Values strictly below the first power are returned as plain integers.
    assert intword(999) == "999"
```


---- revisão ----

Notes: `intword(1000) == "1.0 thousand"` is stated verbatim in the issue; `-1000` and `999` are trace-derived from the same code path and the unchanged-below-power guard, so all three are kept.

```python
from alvo import intword


def test_intword_1000_is_humanized():
    assert intword(1000) == "1.0 thousand"


def test_intword_negative_1000_is_humanized():
    assert intword(-1000) == "-1.0 thousand"


def test_intword_below_power_is_unchanged():
    assert intword(999) == "999"
```