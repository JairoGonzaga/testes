Analysis:
- The issue promises `ordinal(111) == '111th'`; currently it returns `'111st'` because only `(11,12,13)` are special-cased, not numbers whose last two digits are 11/12/13.
- Expected values come from the issue text: `111 -> '111th'`.
- I'll also assert the stated-good small case `11 -> '11th'` (matches current special-case) to pin the suffix table, and closely-related 112/113 as the same class of bug — the issue says numbers ending in 11/12/13 get wrong suffix, so 112 -> '112th', 113 -> '113th' follow from the promised rule.
- Keep it small per instructions.

```python
import pytest

from alvo import ordinal


def test_ordinal_111_is_111th():
    assert ordinal(111) == "111th"


def test_ordinal_11_still_works():
    assert ordinal(11) == "11th"


@pytest.mark.parametrize(
    "value, expected",
    [
        (112, "112th"),
        (113, "113th"),
    ],
)
def test_other_teens_suffixes(value, expected):
    assert ordinal(value) == expected
```

---- revisão ----

Notes: `112`/`113` expected values are not stated by the issue (only `111`), so I drop them; `111 -> '111th'` is stated and `11 -> '11th'` is verified by tracing the current code, so both are kept.

```python
from alvo import ordinal


def test_ordinal_111_is_111th():
    assert ordinal(111) == "111th"


def test_ordinal_11_still_works():
    assert ordinal(11) == "11th"
```