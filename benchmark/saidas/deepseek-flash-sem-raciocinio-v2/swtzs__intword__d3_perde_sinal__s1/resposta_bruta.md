Analysis: `intword` is documented by the issue to keep the minus sign, e.g. `intword(-1000000) == '-1.0 million'`. The bug is that the negative branch sets `negative_prefix = ""` instead of `"-"`. Expected values come straight from the issue text (`-1.0 million`), and by the same stated rule `intword(-1000) == '-1.0 thousand'` and `intword(-5) == '-5'`. Also `_format_not_finite` gives `-Inf`, consistent with negative handling.

```python
import pytest

from alvo import intword


def test_intword_negative_million_keeps_minus():
    assert intword(-1000000) == "-1.0 million"


def test_intword_negative_thousand_keeps_minus():
    assert intword(-1000) == "-1.0 thousand"


def test_intword_negative_small_keeps_minus():
    assert intword(-5) == "-5"
```

---- revisão ----

Notes: `-1.0 million` is from the issue; `-1.0 thousand` follows from the same stated sign rule by tracing `value<powers[0]` branch (1000 is not `< powers[0]`=1000, so unit path gives "thousand"); `-5` traces the `value < powers[0]` branch returning the value with sign. All three fail now (prefix is `""`) and pass with minimal fix (`negative_prefix = "-"`).

```python
import pytest

from alvo import intword


def test_intword_negative_million_keeps_minus():
    assert intword(-1000000) == "-1.0 million"


def test_intword_negative_thousand_keeps_minus():
    assert intword(-1000) == "-1.0 thousand"


def test_intword_negative_small_keeps_minus():
    assert intword(-5) == "-5"
```