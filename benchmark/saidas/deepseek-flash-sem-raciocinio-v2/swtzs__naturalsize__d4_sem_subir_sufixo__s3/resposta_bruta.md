```python
from alvo import naturalsize


def test_naturalsize_rounds_up_to_next_unit():
    # Issue: 999999 bytes -> rounds to 1000.0 kB, should promote to 1.0 MB
    assert naturalsize(999999) == '1.0 MB'
```


---- revisão ----

The single assertion matches the issue's stated input (999999) and expected output ('1.0 MB'); it fails now because current code returns '1000.0 kB' and passes after the minimal unit-promotion fix.

```python
from alvo import naturalsize


def test_naturalsize_rounds_up_to_next_unit():
    assert naturalsize(999999) == '1.0 MB'
```