Analysis:
- The issue states `validate('79927398713')` must return `'79927398713'` because its Luhn check digit is valid.
- The current `checksum` function computes the standard Luhn sum but returns it mod `n`; for a valid Luhn number the sum (after doubling/divmod) should be a multiple of 10, so `checksum == 0`.
- Let me trace: values reversed for `79927398713` are `[3,1,7,8,9,3,7,2,9,9,7]`. Odd indices (1-based doubling of alternates): indices 1,3,5,7,9 → `1,8,3,2,9`; doubled sums: `sum(divmod(2,10))=2, 8*2=16→1+6=7, 3*2=6, 2*2=4, 9*2=18→9` = `2+7+6+4+9=28`. Even indices: `3,7,9,7,9,7` = `42`. Total = 70. 70 % 10 = 0. So `checksum` should be 0.
- The bug must be in the slicing: `values[1::2]` are the doubled positions normally, and `values[::2]` are the non-doubled. The standard algorithm doubles every second digit starting from the second-to-last (rightmost), i.e. indices 1,3,5,... in the reversed array. So `values[1::2]` should be doubled, and `values[::2]` summed plainly. But the code does the opposite.
- Wait — but then 70 would still be 70 either way? Actually no: doubling `42` vs doubling `28` differs since `sum(divmod(i*2,10))` is not linear. Doubling `[3,7,9,7,9,7]` gives `6+5+9+5+9+5=39` plus `28` = `67`, 67 % 10 = 7 ≠ 0 → rejected. Doubling `[1,8,3,2,9]` gives `2+7+6+4+9=28` plus `42` = `70`, % 10 = 0 → valid.
- So the correct algorithm (double indices 1,3,5,...) gives 0; the code's swapped version gives 7. The fix is to swap the slices. The test should assert `validate('79927398713') == '79927398713'`.
- The issue also states the exception type currently raised is `InvalidChecksum`, so we can assert no exception (or specifically that it doesn't raise). I'll keep it minimal: one test for the return value, and one confirming no `InvalidChecksum` is raised.

```python
import pytest

from alvo import validate, InvalidChecksum


def test_validate_textbook_luhn_number_returns_number():
    assert validate('79927398713') == '79927398713'


def test_validate_textbook_luhn_number_does_not_raise():
    try:
        result = validate('79927398713')
    except InvalidChecksum:
        pytest.fail("valid Luhn number was rejected with InvalidChecksum")
    assert result == '79927398713'
```

---- revisão ----

Notes: Both assertions are stated by the issue (return value `'79927398713'`, and that it currently raises `InvalidChecksum`); both fail now and pass after the fix. Keeping both is fine but the second is redundant—I'll keep only the direct, issue-stated return-value test plus an explicit "does not raise InvalidChecksum" assertion, which the issue directly describes.

```python
import pytest

from alvo import validate


def test_validate_textbook_luhn_number_returns_number():
    assert validate('79927398713') == '79927398713'


def test_validate_textbook_luhn_number_does_not_raise_invalid_checksum():
    from alvo import InvalidChecksum
    try:
        assert validate('79927398713') == '79927398713'
    except InvalidChecksum:
        pytest.fail("valid Luhn number was rejected with InvalidChecksum")
```