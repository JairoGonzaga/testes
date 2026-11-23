I traced `ordinal(11)`: `11 % 10 == 1` which is "not" in `(11,12,13)` (a 10% value is 0..9), so `digit=1` → `'11st'`, while the issue wants `'11th'`. The minimal fault is comparing the last digit against two-digit values. Expected values for the nearby cases come from the ordinary English convention the `_SUFIXOS` table encodes (11th/12th/13th, 21st, 22nd, 23rd, 24th) plus the non-finite handling directly visible in the source.

```python
from alvo import ordinal


def test_eleven_is_th():
    # Inputs/expected value come directly from the issue report.
    assert ordinal(11) == "11th"


def test_other_teen_numbers_are_th():
    assert ordinal(12) == "12th"
    assert ordinal(13) == "13th"


def test_normal_ordinal_suffixes():
    assert ordinal(1) == "1st"
    assert ordinal(2) == "2nd"
    assert ordinal(3) == "3rd"
    assert ordinal(4) == "4th"
    assert ordinal(10) == "10th"
    assert ordinal(21) == "21st"
    assert ordinal(22) == "22nd"
    assert ordinal(23) == "23rd"


def test_not_finite_values():
    # Expected values are stated explicitly by _format_not_finite in the source.
    assert ordinal(float("nan")) == "NaN"
    assert ordinal(float("inf")) == "+Inf"
    assert ordinal(float("-inf")) == "-Inf"
```

---- revisão ----

Notes: The issue explicitly promises `ordinal(11) -> '11th'`; I trace 12/13 through `else value % 10` (0/1/2 of `_SUFIXOS`) to get `12th`/`13th` (all tie to the same buggy `in (11,12,13)` predicate and pass with the minimal fix). I drop all other assertions: `21/22/23` either pass on the buggy code or depend on a fix choice (1 vs 11), and the non-finite cases aren't related to the reported bug nor cited by the task.

```python
from alvo import ordinal


def test_eleven_is_th():
    # Expected value quoted directly from the issue report.
    assert ordinal(11) == "11th"


def test_teen_numbers_are_th():
    # Expected values obtained by tracing the code line by line; they share
    # the same faulty `value % 10 in (11, 12, 13)` predicate as the issue,
    # so they fail now and pass after the minimal fix.
    assert ordinal(12) == "12th"
    assert ordinal(13) == "13th"
```