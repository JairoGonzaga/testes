```python
from alvo import naturalsize


def test_binary_uses_powers_of_1024_for_issue_example():
    assert naturalsize(3_000_000, binary=True) == "2.9 MiB"


def test_binary_does_not_switch_to_kibibytes_below_1024_bytes():
    assert naturalsize(1023, binary=True) == "1023 Bytes"


def test_binary_one_gibibyte_is_exactly_one_gibibyte():
    assert naturalsize(1024**3, binary=True) == "1.0 GiB"
```