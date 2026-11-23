Analysis:
- Issue states only one concrete case: `naturalsize(999999)` currently gives `'1000.0 kB'`, expected `'1.0 MB'`.
- Expected value `'1.0 MB'` comes directly from the issue text.
- Suffix for decimal is taken from module (`MB` is `suffix[1]`); formatting `999999/1000**2 = 0.999999` with `"%.1f"` yields `"1.0"` by round-half-even/rounding rules (well above 0.95), so `'1.0 MB'`.
- Test just asserts the reported output, so it fails now and passes after promoting the exponent.

```python
from alvo import naturalsize


def test_naturalsize_rounds_up_to_next_unit():
    assert naturalsize(999999) == "1.0 MB"
```

---- revisão ----

Only the one assertion is in the file; it matches the issue’s stated input/output, fails currently (`'1000.0 kB'`), and passes once the unit is promoted to `'1.0 MB'`. No changes needed.

```python
from alvo import naturalsize


def test_naturalsize_rounds_up_to_next_unit():
    assert naturalsize(999999) == "1.0 MB"
```