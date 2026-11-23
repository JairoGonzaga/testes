## Analysis

The issue promises `ordinal(111) == '111th'` because 111 ends in 11 (a teen). The code only checks `value in (11, 12, 13)`, so 111 falls through to `value % 10 == 1` → `"st"`. Expected values come directly from the issue and the source: `_SUFIXOS[1]='st'`, `_SUFIXOS[3]='rd'`, `_SUFIXOS[0]='th'`. The fix should make numbers ending in 11/12/13 use "th"; small working cases (11, 12, 13, 1, 2, 3) must stay correct. Tests assert exact strings from the issue/source.

```python
import pytest

from alvo import ordinal


def test_ordinal_111_is_th():
    # Reported in the issue: ordinal(111) must be '111th'.
    assert ordinal(111) == "111th"


def test_ordinal_teens_larger_than_13_end_in_th():
    # Numbers whose last two digits are 11/12/13 take 'th' (per issue intent).
    assert ordinal(112) == "112th"
    assert ordinal(113) == "113th"


def test_ordinal_small_values_still_work():
    # Values stated as already correct in the issue / by the source table.
    assert ordinal(11) == "11th"
    assert ordinal(12) == "12th"
    assert ordinal(13) == "13th"
    assert ordinal(1) == "1st"
    assert ordinal(2) == "2nd"
    assert ordinal(3) == "3rd"
    assert ordinal(4) == "4th"
```

---- revisão ----

Notes: The 111 case is stated explicitly; 112/113 follow only from my "ends in 11/12/13" interpretation of the fix (not stated), so drop them; 11/12/13/1/2/3/4 are already correct per the source table and are safe to keep. Corrected file:

```python
from alvo import ordinal


def test_ordinal_111_is_th():
    # Reported in the issue: ordinal(111) must be '111th'.
    assert ordinal(111) == "111th"


def test_ordinal_small_values_still_work():
    # Values stated as already correct in the issue / by the source table.
    assert ordinal(11) == "11th"
    assert ordinal(12) == "12th"
    assert ordinal(13) == "13th"
    assert ordinal(1) == "1st"
    assert ordinal(2) == "2nd"
    assert ordinal(3) == "3rd"
    assert ordinal(4) == "4th"
```