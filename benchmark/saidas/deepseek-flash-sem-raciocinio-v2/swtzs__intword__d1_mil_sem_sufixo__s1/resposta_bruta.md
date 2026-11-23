```python
from alvo import intword


def test_intword_1000():
    assert intword(1000) == "1.0 thousand"
```

---- revisão ----

The only assertion matches the issue exactly: `intword(1000)` is expected to be `'1.0 thousand'` as stated in the report, and it fails now the code returns `'1000'` (due to `value <= powers[0]`) and passes when that boundary is corrected to `<`.

```python
from alvo import intword


def test_intword_1000():
    assert intword(1000) == "1.0 thousand"
```