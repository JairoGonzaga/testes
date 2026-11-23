```python
import pytest

from alvo import ordinal


def test_ordinal_11():
    assert ordinal(11) == "11th"


def test_ordinal_12():
    assert ordinal(12) == "12th"


def test_ordinal_13():
    assert ordinal(13) == "13th"


def test_ordinal_111():
    assert ordinal(111) == "111th"


def test_ordinal_112():
    assert ordinal(112) == "112th"


def test_ordinal_113():
    assert ordinal(113) == "113th"


def test_ordinal_211():
    assert ordinal(211) == "211th"


def test_ordinal_1011():
    assert ordinal(1011) == "1011th"
```