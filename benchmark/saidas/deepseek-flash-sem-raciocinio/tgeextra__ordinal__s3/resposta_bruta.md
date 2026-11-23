```python
import pytest

from alvo import ordinal


def test_c37_r6_negative_ordinal():
    # [R1/negativo] negative values use the same suffix rules
    assert ordinal(-1) == '-1th'
    assert ordinal(-2) == '-2th'
    assert ordinal(-11) == '-11th'
```
```python
import pytest

from alvo import ordinal


def test_c37_r6_negative_ordinal():
    # [R1/negativo] negative values: -1 % 10 == 9, -2 % 10 == 8, so suffix 'th'
    assert ordinal(-1) == '-1th'
    assert ordinal(-2) == '-2th'
    assert ordinal(-11) == '-11th'
    assert ordinal(-22) == '-22th'
```