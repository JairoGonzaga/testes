Analysis:
- The issue states `intword(999999)` must return `'1.0 million'`, not `'1000.0 thousand'`.
- Root cause: when rounding pushes the value to the next power, `ordinal` is incremented but `unit` is taken from `human_powers[ordinal]` after increment — actually in current code `rounded_value = 1.0` is set, but `power`/`unit` use `ordinal` after increment. Let me trace: ordinal = bisect_right(powers, 999999). powers[0]=1000, powers[1]=1e6. 999999 < 1e6, so bisect_right returns 1. largest_ordinal = (1 == 12)? No. ordinal -= 1 → 0. power=1000. chopped=999.999. rounded_value=float("%.1f" % 999.999)=1000.0. Not largest, rounded_value == powers[1] (1e6)? 1000.0 != 1000000.0. So no promotion. unit="thousand", number="1000.0" → bug.
- The check compares rounded_value to `powers[ordinal+1]` but rounded_value is in chopped units, not absolute. It should compare to `powers[ordinal+1]/power` i.e. 1000. Then promote to ordinal 1, rounded_value=1.0, unit million.
- Expected: `intword(999999) == '1.0 million'`.
- A closely related case stated implicitly: same rounding-promotion mechanism. The issue only states this one example, plus the mechanism (rounding pushes to next power). I'll include 999999 → '1.0 million' and maybe 999999999 → '1.0 billion' (same mechanism, traced: chopped=999.999999, rounded=1000.0, should promote to billion).

Let me trace 999999999: bisect_right(powers, 999999999): powers[2]=1e9 > value, so returns 2. ordinal-=1 → 1. power=1e6. chopped=999.999999. rounded="%.1f" → 1000.0. Should promote: ordinal=2, rounded=1.0, unit=billion → '1.0 billion'.

Keep it small. Include the issue example and one closely related case using the same stated mechanism.

```python
from alvo import intword


def test_intword_rounds_up_to_next_power():
    # Issue: rounding pushed value to 1000.0 thousand; expected promotion to million.
    assert intword(999999) == '1.0 million'


def test_intword_rounds_up_through_billion():
    # Same rounding-promotion mechanism as reported in the issue.
    assert intword(999999999) == '1.0 billion'
```

---- revisão ----

Notes: The issue states only `intword(999999) == '1.0 million'`; my second case (999999999 → '1.0 billion') is an extrapolation from the same mechanism but its expected value is not stated by the task, so I delete it to keep the test strictly on the reported behavior.

```python
from alvo import intword


def test_intword_rounds_up_to_next_power():
    # Issue: rounding pushed 999999 to "1000.0 thousand"; expected "1.0 million".
    assert intword(999999) == '1.0 million'
```