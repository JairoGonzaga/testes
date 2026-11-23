```python
# test_issue.py
#
# This test reproduces the bug reported in the issue: a known valid CPF
# number is rejected with InvalidChecksum.  The test checks that
# `validate` returns the cleaned CPF string.  Under the current buggy
# implementation the call raises InvalidChecksum, causing the test to
# fail.  After the bug is fixed, the test will pass.

import pytest
from alvo import validate, InvalidChecksum


def test_valid_cpf_is_not_rejected():
    """A known valid CPF should return the compacted string."""
    # The CPF 111.444.777-35 is known to be valid.  The compacted form is
    # '11144477735'.
    assert validate('11144477735') == '11144477735'
```

---- revisão ----

The test correctly asserts the behaviour described in the issue: it verifies that the valid CPF “11144477735” is returned as is, which currently fails because the code raises InvalidChecksum, but will pass once the bug is fixed.  

```python
# test_issue.py
#
# This test reproduces the bug reported in the issue: a known valid CPF
# number is rejected with InvalidChecksum.  The test checks that
# `validate` returns the cleaned CPF string.  Under the current buggy
# implementation the call raises InvalidChecksum, causing the test to
# fail.  After the bug is fixed, the test will pass.

import pytest
from alvo import validate, InvalidChecksum


def test_valid_cpf_is_not_rejected():
    """A known valid CPF should return the compacted string."""
    # The CPF 111.444.777-35 is known to be valid.  The compacted form is
    # '11144477735'.
    assert validate('11144477735') == '11144477735'
```