## Analysis

The issue states: `intword(999999)` currently returns `'1000.0 thousand'`, but expected `'1.0 million'`.

Tracing the code for `value = 999999`:
- `value >= powers[0]` (1000), so we `bisect_right(powers, 999999)` → `ordinal = 1`, `largest_ordinal = False`.
- `ordinal -= 1` → `0`, `power = 1000`, `chopped = 999.999`.
- `rounded_value = float("%.1f" % 999.999)` = `1000.0`.
- The promotion check compares `rounded_value == powers[ordinal + 1]`, i.e. `1000.0 == 10**6 = 1000000` → **False**. So no promotion → `'1000.0 thousand'`.

The bug: the promotion condition compares the *chopped/rounded* value to the next absolute power, but `rounded_value` is already scaled down by `power`. It should compare to the next power *divided by* `power`, i.e. `powers[ordinal+1] / power`. For the issue's case, `10**6 / 10**3 = 1000.0`, and `rounded_value == 1000.0` → promotion to `1.0 million`.

The tests only assert the issue's stated input/output plus the already-correct small case.

```python
from alvo import intword


def test_intword_999999_promotes_to_million():
    # Issue: intword(999999) returns '1000.0 thousand', expected '1.0 million'.
    assert intword(999999) == "1.0 million"


def test_intword_999_stays_plain():
    # Value below first power is returned unchanged (as documented by code).
    assert intword(999) == "999"
```


---- revisão ----

Notes: `test_intword_999999_promotes_to_million` matches the issue exactly (fails now, passes after fix). `test_intword_999_stays_plain` is traced from code (`999 < 1000` returns `f"999"`), but it is an unrelated case not tied to the bug; the task says keep it small and only closely related cases with expected values stated by the issue — the issue states no such value, so delete it.

```python
from alvo import intword


def test_intword_999999_promotes_to_million():
    # Issue: intword(999999) returns '1000.0 thousand', expected '1.0 million'.
    assert intword(999999) == "1.0 million"
```