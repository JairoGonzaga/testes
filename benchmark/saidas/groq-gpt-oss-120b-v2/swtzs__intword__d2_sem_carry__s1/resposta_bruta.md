**Explanation**

`intword` should promote the suffix when rounding pushes the value to the next power.
For the input `999 999` the correct output is `"1.0 million"` (value `1.0` and the
next unit), but the current implementation returns `"1000.0 thousand"`.
The test below asserts the expected output, causing a failure on the existing
code and a pass once the bug is fixed.

```python
import pytest
from alvo import intword


def test_intword_rounded_up_to_next_power():
    """
    When rounding a number pushes it to the next power of thousand,
    the suffix must be promoted.

    999 999 → 1.0 million
    """
    assert intword(999999) == "1.0 million"
```

---- revisão ----

All assertions match the behavior described in the issue and use the expected value quoted directly from the task.  

```python
import pytest
from alvo import intword


def test_intword_rounded_up_to_next_power():
    """
    Verify that rounding a number that reaches the next power promotes the suffix.

    Input: 999999
    Expected output (as stated in the issue): "1.0 million"
    """
    assert intword(999999) == "1.0 million"
```