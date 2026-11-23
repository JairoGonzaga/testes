```python
# test_issue.py

from alvo import naturalsize


def test_positive_one():
    """
    Verify that the singular form is used for the positive value 1.
    """
    assert naturalsize(1) == "1 Byte"


def test_negative_one():
    """
    Verify that the singular form is also used for the negative value -1.
    The current implementation incorrectly returns '-1 Bytes',
    while the issue specifies that it should be '-1 Byte'.
    """
    assert naturalsize(-1) == "-1 Byte"
```

---- revisão ----

No changes needed.  

```python
# test_issue.py

from alvo import naturalsize


def test_positive_one():
    """
    Verify that the singular form is used for the positive value 1.
    """
    assert naturalsize(1) == "1 Byte"


def test_negative_one():
    """
    Verify that the singular form is also used for the negative value -1.
    The current implementation incorrectly returns '-1 Bytes',
    while the issue specifies that it should be '-1 Byte'.
    """
    assert naturalsize(-1) == "-1 Byte"
```