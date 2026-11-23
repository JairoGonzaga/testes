Analysis:
- Issue: `ordinal(13)` must return `'13th'`; 11, 12, 13 always take 'th'.
- Current code excludes only 11 and 12 from the digit-based suffix: `value % 100 in (11, 12)`. For 13, digit becomes 3 → `'rd'`.
- Fix will add 13 to that tuple, making digit 0 → `_SUFIXOS[0] == 'th'`.
- Expected values from issue text: `ordinal(13) == '13th'`, plus 11 and 12 always 'th' (e.g. `ordinal(11) == '11th'`, `ordinal(12) == '12th'`).
- Also include a closely related case 113 ('th' per code after fix) — but issue only states 11,12,13; keep minimal, assert 111/112/113 via same rule? Issue says "11, 12 and 13 always take 'th'". I'll assert 13 mainly and 11, 12 as stated.

```python
from alvo import ordinal


def test_ordinal_13_is_th():
    assert ordinal(13) == "13th"


def test_ordinal_11_is_th():
    assert ordinal(11) == "11th"


def test_ordinal_12_is_th():
    assert ordinal(12) == "12th"
```

---- revisão ----

Notes: `13th` is stated in the issue; 11/12 "always take 'th'" is also stated. Keep all three — minimal fix (adding 13 to the tuple) makes all pass; only the 13 test fails now.

```python
from alvo import ordinal


def test_ordinal_13_is_th():
    assert ordinal(13) == "13th"


def test_ordinal_11_is_th():
    assert ordinal(11) == "11th"


def test_ordinal_12_is_th():
    assert ordinal(12) == "12th"
```