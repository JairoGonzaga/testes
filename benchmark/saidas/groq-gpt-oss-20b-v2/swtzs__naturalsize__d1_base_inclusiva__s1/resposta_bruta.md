```python
# test_issue.py
import pytest
from alvo import naturalsize


def test_naturalsize_kilobyte_conversion():
    """
    The natural size of 1000 bytes should be expressed in kilobytes,
    not left as a raw byte count.  The default behaviour uses a
    decimal base (1000) and the suffix "kB".
    """
    # The current buggy implementation returns "1000 Bytes".
    # After the minimal fix it should return "1.0 kB".
    assert naturalsize(1000) == "1.0 kB"

    # A value just below the threshold should still be shown in bytes.
    assert naturalsize(999) == "999 Bytes"


def test_naturalsize_boundary_for_gnu_and_binary():
    """
    The boundary handling differs for the `gnu` and `binary` flags.
    These cases are not part of the reported bug but confirm that
    the function behaves consistently for them.
    """
    # With GNU mode, the base is 1024 and the suffixes are single letters.
    assert naturalsize(1000, gnu=True) == "1000B"

    # With binary mode, the base is also 1024 but suffixes are KiB, MiB, ...
    assert naturalsize(1000, binary=True) == "1000 Bytes"
```

---- revisão ----

The assertions are all consistent with the code or the task; each expected value comes directly from the code’s logic or the issue statement.

```python
# test_issue.py
import pytest
from alvo import naturalsize


def test_naturalsize_kilobyte_conversion():
    """
    The natural size of 1000 bytes should be expressed in kilobytes,
    not left as a raw byte count.  The default behaviour uses a
    decimal base (1000) and the suffix "kB".
    """
    # The current buggy implementation returns "1000 Bytes".
    # After the minimal fix it should return "1.0 kB".
    assert naturalsize(1000) == "1.0 kB"

    # A value just below the threshold should still be shown in bytes.
    assert naturalsize(999) == "999 Bytes"


def test_naturalsize_boundary_for_gnu_and_binary():
    """
    The boundary handling differs for the `gnu` and `binary` flags.
    These cases confirm that the function behaves consistently for them.
    """
    # With GNU mode, the base is 1024 and the suffixes are single letters.
    assert naturalsize(1000, gnu=True) == "1000B"

    # With binary mode, the base is also 1024 but suffixes are KiB, MiB, ...
    assert naturalsize(1000, binary=True) == "1000 Bytes"
```