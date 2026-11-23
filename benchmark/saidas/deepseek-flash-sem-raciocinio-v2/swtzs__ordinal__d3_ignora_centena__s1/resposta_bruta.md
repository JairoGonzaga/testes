## Analysis

The issue states: `ordinal(111)` must return `'111th'`, but currently returns `'111st'`.
The module's suffix logic checks `value in (11, 12, 13)` for the teen exceptions, but only looks at the last digit `value % 10` otherwise. So `111 % 10 == 1` → `"st"`.
The promised behaviour: numbers whose last two digits are 11/12/13 use `"th"`. Expected value `'111th'` comes directly from the issue text. Closely related stated cases: `11` already works (`'11th'`); consistent extension for 112/113 → `'112th'`, `'113th'`. Also numbers not ending in teens keep their suffix (e.g. `121` → `'121st'`) as the current logic already produces, so we avoid asserting anything more.

```python
from alvo import ordinal


def test_ordinal_111_is_111th():
    assert ordinal(111) == "111th"


def test_ordinal_111_still_wrong_suffix_is_th():
    # report: expected '111th', currently '111st'
    assert ordinal(111) != "111st"


def test_ordinal_112_and_113_are_th():
    assert ordinal(112) == "112th"
    assert ordinal(113) == "113th"


def test_small_teens_still_work():
    assert ordinal(11) == "11th"
    assert ordinal(12) == "12th"
    assert ordinal(13) == "13th"
```


---- revisão ----

Notes: `111 != "111st"` duplicates the first test and is redundant; drop it. Keep `111th` (stated), `112th`/`113th` (same teen-suffix rule the fix applies, verified by tracing `value % 100 in (11,12,13)`), and the already-working 11/12/13.

```python
from alvo import ordinal


def test_ordinal_111_is_111th():
    assert ordinal(111) == "111th"


def test_ordinal_112_and_113_are_th():
    assert ordinal(112) == "112th"
    assert ordinal(113) == "113th"


def test_small_teens_still_work():
    assert ordinal(11) == "11th"
    assert ordinal(12) == "12th"
    assert ordinal(13) == "13th"
```