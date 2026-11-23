I need to reproduce the bug: `validate('00000000000')` currently returns `'00000000000'` instead of raising `InvalidFormat`. Per the issue, the expected behavior is that `InvalidFormat` is raised. Note the checksum for all-zeros is `'00'`, which equals the last two chars, so the bug only shows up as a missing all-zeros rejection. I'll also add a valid CPF (from the well-known example `529.982.247-25`, compacting to `52998224725`) to guard against a fix that rejects everything, keeping the fix minimal and passing. The padding in valid/non-valid fixtures does not change the compacted result here.

```python
import pytest

from alvo import InvalidFormat, validate


def test_all_zeros_cpf_rejected():
    # The all-zeros CPF must be rejected with InvalidFormat.
    with pytest.raises(InvalidFormat):
        validate("00000000000")


def test_valid_cpf_still_accepted():
    # A genuinely valid CPF must keep working (guards against an
    # over-eager fix that rejects all numbers).
    assert validate("529.982.247-25") == "52998224725"


def test_non_allzero_repeating_digits_rejected():
    # A repeating-digit CPF (not all zeros) is also invalid → checksum fail.
    with pytest.raises(Exception):
        validate("12312312312")
```

---- revisão ----

Review of each assertion:
1. `test_all_zeros_cpf_rejected`: Expected (`InvalidFormat`) is copied verbatim from the issue, which even shows it currently returns `'00000000000'`. Fails now due to the bug; after a minimal all-zeros guard in `validate()` it raises `InvalidFormat` → passes. KEEP.
2. `test_valid_cpf_still_accepted`: `52998224725` is a memorized CPF and its checksum is not stated in the task → violates rule 2. DELETE.
3. `test_non_allzero_repeating_digits_rejected`: `12312312312` is out of scope (not mentioned in the issue) and "real-world convention" → violates rules 1 and 3. DELETE.

```python
import pytest

from alvo import InvalidFormat, validate


def test_all_zeros_cpf_rejected():
    # The issue states validate('00000000000') currently returns
    # '00000000000' but the all-zeros CPF should be rejected with InvalidFormat.
    with pytest.raises(InvalidFormat):
        validate("00000000000")
```