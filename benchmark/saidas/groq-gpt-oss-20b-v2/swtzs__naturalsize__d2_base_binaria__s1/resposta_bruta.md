**Analysis**

The `naturalsize` function is supposed to use a base of 1024 when `binary=True`.  
However, the current implementation always uses a base of 1000 unless `gnu=True`.  
Hence:

* `naturalsize(3000000, binary=True)` incorrectly returns `'3.0 MiB'` (computed with 1000) instead of the expected `'2.9 MiB'` (computed with 1024).  
* Likewise, values such as `2048` are scaled incorrectly.

The test file will check these expected outputs. The test for a decimal value (`1000`) is included to confirm that the decimal logic remains correct.

```python
# test_issue.py
import pytest
from alvo import naturalsize


def test_naturalsize_binary_scaling():
    """
    When binary=True, the function should use powers of 1024.
    3_000_000 bytes ≈ 2.86 MiB → rounded to 2.9 MiB.
    """
    assert naturalsize(3_000_000, binary=True) == "2.9 MiB"


def test_naturalsize_binary_small():
    """
    Small binary values should also be scaled correctly.
    2_048 bytes = 2 KiB (formatted as 2.0 KiB with the default format).
    """
    assert naturalsize(2_048, binary=True) == "2.0 KiB"


def test_naturalsize_binary_exact_mib():
    """
    Exactly one MiB should be reported as 1.0 MiB.
    """
    assert naturalsize(1_048_576, binary=True) == "1.0 MiB"


def test_naturalsize_decimal_base():
    """
    The default decimal (1000) base should produce the expected output.
    """
    assert naturalsize(1_000) == "1.0 kB"
```

These tests will fail with the current buggy implementation and will pass once the base is correctly set to 1024 when `binary=True`.

---- revisão ----

The only required test is the one that checks the binary scaling of 3 000 000 bytes to 2.9 MiB as stated in the issue.

```python
# test_issue.py
import pytest
from alvo import naturalsize


def test_naturalsize_binary_scaling():
    """
    When binary=True, the function should use powers of 1024.
    3_000_000 bytes ≈ 2.86 MiB → rounded to 2.9 MiB.
    """
    assert naturalsize(3_000_000, binary=True) == "2.9 MiB"
```