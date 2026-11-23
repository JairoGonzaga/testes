**Analysis**

The `validate` function should raise `InvalidLength` when the compacted number does not contain exactly 11 digits.  
The issue shows that a 12‑digit CPF (`'111444777350'`) currently raises `InvalidChecksum` because the length check only tests for *less than* 11 digits.  
The test will call `validate` with this 12‑digit value and assert that `InvalidLength` is raised. With the current code the test fails (different exception), and after fixing the length check it will pass.

**Test file (`test_issue.py`)**

```python
import pytest
from alvo import validate, InvalidLength

def test_cpf_with_too_many_digits_raises_invalid_length():
    """
    A CPF longer than 11 digits must raise InvalidLength.
    The current buggy implementation raises InvalidChecksum,
    so this test fails until the bug is fixed.
    """
    with pytest.raises(InvalidLength):
        validate('111444777350')
```

---- revisão ----

All assertions directly reflect the behavior described in the issue and use the exception class named in the task.

```python
import pytest
from alvo import validate, InvalidLength

def test_cpf_with_too_many_digits_raises_invalid_length():
    """
    A CPF longer than 11 digits must raise InvalidLength.
    The current buggy implementation raises InvalidChecksum,
    so this test fails until the bug is fixed.
    """
    with pytest.raises(InvalidLength):
        validate('111444777350')
```