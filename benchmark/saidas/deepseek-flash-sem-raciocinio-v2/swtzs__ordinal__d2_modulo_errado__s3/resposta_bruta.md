Analysis:
- The issue promises `ordinal(11) == '11th'` (and by the same rule, 12th, 13th, and any number ending in 11/12/13).
- The buggy line is `digit = 0 if value % 10 in (11, 12, 13) else value % 10`; `value % 10` can never be 11/12/13, so the special case never triggers.
- Expected values from task text: 11 → '11th'. Closely related teens cases (12, 13) follow the same stated rule; 1 → '1st', 2 → '2nd', 3 → '3rd' come from the suffixed table.
- I will only assert the teens cases stated/implied by the issue plus a couple of basic suffix sanity cases from the `_SUFIXOS` tuple (no mental-computation constants beyond these).

```python
import pytest

from alvo import ordinal


def test_ordinal_11_is_11th():
    assert ordinal(11) == "11th"


def test_ordinal_12_and_13_are_teens():
    assert ordinal(12) == "12th"
    assert ordinal(13) == "13th"


def test_ordinal_111_and_112_are_teens():
    assert ordinal(111) == "111th"
    assert ordinal(112) == "112th"


def test_ordinal_basic_suffixes():
    # sanity: these come straight from the _SUFIXOS table
    assert ordinal(1) == "1st"
    assert ordinal(2) == "2nd"
    assert ordinal(3) == "3rd"
    assert ordinal(4) == "4th"
```

---- revisão ----

Notes: `ordinal(11)` is stated; 12/13 and 111/112 follow from the same teen rule (trace: buggy code gives 12th already? no—`%10=2`→'12nd', so it fails; fixed gives '12th'); the 1st/2nd/3rd/4th cases trace directly from `_SUFIXOS` and already pass, so they're harmless but not needed—kept only 1 and 4 style sanity is fine; I'll trim to the issue plus teen rule cases whose expected values are clear.

```python
import pytest

from alvo import ordinal


def test_ordinal_11_is_11th():
    assert ordinal(11) == "11th"


def test_ordinal_12_and_13_are_teens():
    assert ordinal(12) == "12th"
    assert ordinal(13) == "13th"


def test_ordinal_111_and_112_are_teens():
    assert ordinal(111) == "111th"
    assert ordinal(112) == "112th"
```