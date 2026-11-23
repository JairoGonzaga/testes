Analysis:
- The issue promises `ordinal(11) == '11th'`; currently the code computes `value % 10` (which is 1 for 11) and never checks `value % 100`.
- Expected values come directly from the issue: 11 → '11th'. Closely related cases stated by the standard English rule the code intends: 12 → '12th', 13 → '13th' (teens) and 21 → '21st' (non-teen ending in 1). The suffix table `_SUFIXOS[3]` is 'rd', so 23 → '23rd'.
- `ordinal(1)` → '1st' via the table: index 1 = 'st'.
- The bug is in `digit = 0 if value % 10 in (11, 12, 13) else value % 10`, which should test `value % 100`.

```python
import pytest

from alvo import ordinal


def test_ordinal_11_is_th():
    assert ordinal(11) == '11th'


def test_ordinal_teens_are_th():
    assert ordinal(12) == '12th'
    assert ordinal(13) == '13th'


def test_ordinal_21_is_st():
    assert ordinal(21) == '21st'
```


---- revisão ----

Notes: Only `ordinal(11) == '11th'` is stated by the issue; 12/13/21 are standard-rule assumptions not given in the task, so I delete them and keep the single stated case.

```python
import pytest

from alvo import ordinal


def test_ordinal_11_is_th():
    assert ordinal(11) == '11th'
```