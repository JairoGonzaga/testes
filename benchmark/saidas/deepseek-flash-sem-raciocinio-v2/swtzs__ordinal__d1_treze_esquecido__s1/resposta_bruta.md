## Analysis

The issue says 11, 12 and 13 always take 'th'. The expected `ordinal(13) == '13th'` comes directly from the issue text.

Tracing the code: `digit = 0 if value % 100 in (11, 12) else value % 10`. For 13, `13 % 100 == 13`, not in `(11, 12)`, so `digit = 13 % 10 = 3` → `_SUFIXOS[3] == "rd"` → `"13rd"` (bug). For 11 and 12, digit is 0 → "th" (works).

A fix must include 13 in the tuple `(11, 12, 13)`. The tests assert the issue's stated cases: 11, 12, 13 all take 'th', plus one representative case outside the teens (e.g. 1 → '1st', 2 → '2nd', 3 → '3rd') to pin the fix without overreaching.

```python
import pytest

from alvo import ordinal


def test_ordinal_11_is_th():
    assert ordinal(11) == "11th"


def test_ordinal_12_is_th():
    assert ordinal(12) == "12th"


def test_ordinal_13_is_th():
    # Reproduces the reported bug: currently returns '13rd'.
    assert ordinal(13) == "13th"


@pytest.mark.parametrize(
    "value,expected",
    [
        (1, "1st"),
        (2, "2nd"),
        (3, "3rd"),
    ],
)
def test_ordinal_basic_suffixes(value, expected):
    assert ordinal(value) == expected
```

---- revisão ----

Notes: `13th` is stated in the issue; `11th`/`12th` are stated ("11, 12 and 13 always take 'th'"); the `1st/2nd/3rd` params are verified by tracing the code (`_SUFIXOS`), all pass before and after the fix—keep.

```python
import pytest

from alvo import ordinal


def test_ordinal_11_is_th():
    assert ordinal(11) == "11th"


def test_ordinal_12_is_th():
    assert ordinal(12) == "12th"


def test_ordinal_13_is_th():
    # Reproduces the reported bug: currently returns '13rd'.
    assert ordinal(13) == "13th"


@pytest.mark.parametrize(
    "value,expected",
    [
        (1, "1st"),
        (2, "2nd"),
        (3, "3rd"),
    ],
)
def test_ordinal_basic_suffixes(value, expected):
    assert ordinal(value) == expected
```