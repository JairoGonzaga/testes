Analysis: The issue promises `ordinal(11) == '11th'` (and by the same 11–13 rule, `12th`, `13th`). The module computes `value % 10 in (11, 12, 13)` which is never true for a single digit, so 11→'11st', 12→'12nd', 13→'13rd'. The intended check is on the last two digits (`value % 100`). Expected values come directly from the issue: `'11th'`, plus the standard companions `'12th'`/`'13th'` implied by the same stated rule.

```python
from alvo import ordinal


def test_ordinal_11_is_th():
    assert ordinal(11) == "11th"


def test_ordinal_12_is_th():
    assert ordinal(12) == "12th"


def test_ordinal_13_is_th():
    assert ordinal(13) == "13th"
```

---- revisão ----

Notes: Only `ordinal(11) == '11th'` is stated by the issue; the `12th`/`13th` cases are my own extension, so I delete them. This single test fails now (`'11st'`) and passes after the minimal `% 100` fix.

```python
from alvo import ordinal


def test_ordinal_11_is_th():
    assert ordinal(11) == "11th"
```