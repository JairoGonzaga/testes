Analysis:
- `apnumber` is documented (issue) to spell out single-digit numbers; expected `apnumber(9) == 'nine'`.
- The bug is the upper bound check `not 0 <= value < 9`, which excludes 9.
- The words table contains "nine" at index 9, so the fix is to allow `value <= 9` (i.e. `value < 10`).
- Expected values come straight from the issue: 9 → 'nine' (and existing behaviour 0..8, 10 stays a digit string).
- 10 is out of range (single-digit), so `'10'` is asserted.

```python
import pytest

from alvo import apnumber


@pytest.mark.parametrize(
    "value, expected",
    [
        (0, "zero"),
        (1, "one"),
        (2, "two"),
        (3, "three"),
        (4, "four"),
        (5, "five"),
        (6, "six"),
        (7, "seven"),
        (8, "eight"),
        (9, "nine"),
    ],
)
def test_apnumber_spells_single_digits(value, expected):
    assert apnumber(value) == expected


def test_apnumber_nine_specifically():
    assert apnumber(9) == "nine"


def test_apnumber_ten_is_not_spelled_out():
    assert apnumber(10) == "10"
```

---- revisão ----

Notes: `apnumber(10) == '10'` is not stated by the issue (it only says single-digit; 10's format is my assumption), so delete it; the 0–8 cases are already covered implicitly but harmless—keep only the issue's 9 case plus the closely related single-digit cases 0 and 8 whose expected values come from the code's word table and match the issue's promise.

```python
from alvo import apnumber


def test_apnumber_nine_is_spelled_out():
    assert apnumber(9) == "nine"


def test_apnumber_eight_is_spelled_out():
    assert apnumber(8) == "eight"


def test_apnumber_zero_is_spelled_out():
    assert apnumber(0) == "zero"
```