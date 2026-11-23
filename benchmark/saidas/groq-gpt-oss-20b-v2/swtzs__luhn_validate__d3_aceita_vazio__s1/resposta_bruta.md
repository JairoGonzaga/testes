```python
# test_issue.py
import pytest
from alvo import validate, InvalidFormat

def test_validate_empty_string_raises_invalid_format():
    """
    An empty string should be considered an invalid format and raise
    `InvalidFormat`.  The current implementation incorrectly returns the
    empty string unchanged.
    """
    with pytest.raises(InvalidFormat):
        validate('')
```

---- revisão ----

The test correctly asserts the only behaviour described in the issue: that `validate('')` must raise `InvalidFormat`. It relies on the task’s wording and will fail only due to the reported bug, passing once the minimal fix is applied.  

```python
# test_issue.py
import pytest
from alvo import validate, InvalidFormat

def test_validate_empty_string_raises_invalid_format():
    """
    An empty string should be considered an invalid format and raise
    `InvalidFormat`.  The current implementation incorrectly returns the
    empty string unchanged.
    """
    with pytest.raises(InvalidFormat):
        validate('')
```