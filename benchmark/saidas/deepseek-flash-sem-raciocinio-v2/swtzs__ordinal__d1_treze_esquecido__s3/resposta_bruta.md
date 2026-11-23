## Analysis

The issue states: `ordinal(13)` must return `'13th'`, because "11, 12 and 13 always take 'th'".

Tracing current code for `value = 13`:
- `digit = 0 if 13 % 100 in (11, 12) else 13 % 10` → `13 % 100 == 13`, not in `(11, 12)` → `digit = 13 % 10 = 3`
- `_SUFIXOS[3] = "rd"` → returns `'13rd'` (the bug).

The fix is to include `13` in the special-case set, giving `digit = 0` → `_SUFIXOS[0] = "th"` → `'13th'`.

Expected values taken directly from the issue text: `ordinal(13) == '13th'`, and the stated rule that 11, 12, 13 take 'th'. I also include `ordinal(11) == '11th'` and `ordinal(12) == '12th'` (same stated rule, currently already correct — they won't break either way) to pin the rule. The core failing case is 13 (and its variants like 113 whose tens-digits are also 13 per the `% 100` logic—but the issue only mentions 13, so I keep to what is stated plus 11/12 from the stated rule).

```python
from alvo import ordinal


def test_ordinal_13_is_th():
    # Issue: 11, 12 and 13 always take 'th'.
    assert ordinal(13) == '13th'


def test_ordinal_11_and_12_are_th():
    # Same stated rule: 11, 12 and 13 always take 'th'.
    assert ordinal(11) == '11th'
    assert ordinal(12) == '12th'
```

---- revisão ----

Notes: `ordinal(13) == '13th'` is directly stated by the issue and fails on current code (`'13rd'`), passing with the minimal fix; `ordinal(11)/ordinal(12)` are also supported by the stated rule "11, 12 and 13 always take 'th'" and already pass on current code, so they don't affect reproduction but are consistent — I'll keep only the stated 13 case plus the explicitly stated rule cases, as all are covered by the task text.

```python
from alvo import ordinal


def test_ordinal_13_is_th():
    # Issue: 11, 12 and 13 always take 'th'.
    assert ordinal(13) == '13th'


def test_ordinal_11_and_12_are_th():
    # Same stated rule: 11, 12 and 13 always take 'th'.
    assert ordinal(11) == '11th'
    assert ordinal(12) == '12th'
```