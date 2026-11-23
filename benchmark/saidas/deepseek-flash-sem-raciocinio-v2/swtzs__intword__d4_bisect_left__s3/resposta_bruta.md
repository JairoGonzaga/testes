Analyzing the issue:

- The module has `powers = [10**3, ..., 10**33, 10**100]` (12 entries) and `human_powers` has 12 names ending in `"googol"`.
- `intword(10**100)`: `bisect_left(powers, 10**100)` returns `11` (index of the `10**100` entry). So `ordinal = 11`, `largest_ordinal = (11 == 12)` → `False`.
- But `bisect_left` finds the exact index; when `value == powers[ordinal]`, it should be treated as the largest/last ordinal (or at least not step back). The code decrements to `ordinal = 10` → `power = 10**33` (decillion) and divides, producing the huge number with "decillion".
- A correct value should give `'1.0 googol'`.

The bug: `largest_ordinal = ordinal == len(powers)` is wrong; for exact matches at the last index, `ordinal == len(powers) - 1` should be treated as the last element (no stepping down). Reproduction: `intword(10**100)` should return `'1.0 googol'`.

```python
from alvo import intword


def test_intword_googol():
    assert intword(10**100) == "1.0 googol"


def test_intword_googol_multiple():
    assert intword(2 * 10**100) == "2.0 googol"
```

---- revisão ----

Second test asserts `'2.0 googol'`, but the issue only states `'1.0 googol'` for `intword(10**100)`; the expected value for `2*10**100` is not given by the task, so I remove it.

```python
from alvo import intword


def test_intword_googol():
    assert intword(10**100) == "1.0 googol"
```