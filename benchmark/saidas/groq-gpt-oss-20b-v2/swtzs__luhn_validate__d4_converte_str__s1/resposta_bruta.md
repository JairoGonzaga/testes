```python
# test_issue.py
import pytest
from alvo import validate, InvalidChecksum, InvalidFormat


def test_validate_returns_same_type_for_int():
    """
    The function should return an integer unchanged when the input is an int
    and is a valid Luhn number.
    """
    # This Luhn‑valid number is taken from the issue description.
    number = 79927398713
    result = validate(number)
    assert result == number  # value equality
    assert isinstance(result, int)  # type unchanged


def test_validate_returns_same_type_for_str():
    """
    When a string is supplied the function should return the exact same string.
    """
    number = "79927398713"
    result = validate(number)
    assert result == number
    assert isinstance(result, str)


def test_validate_invalid_checksum_raises():
    """
    Passing a number with an invalid checksum should raise InvalidChecksum.
    """
    # Changing the last digit breaks the checksum.
    invalid_number = 79927398714
    with pytest.raises(InvalidChecksum):
        validate(invalid_number)
```

---- revisão ----

```python
# test_issue.py
import pytest
from alvo import validate, InvalidFormat, InvalidChecksum


def test_validate_returns_same_int_when_valid():
    """
    validate() should return the input integer unchanged when the checksum is valid.
    """
    number = 79927398713
    result = validate(number)
    assert result == number
    assert isinstance(result, int)


def test_validate_returns_same_str_when_valid():
    """
    validate() should return the input string unchanged when the checksum is valid.
    """
    number = "79927398713"
    result = validate(number)
    assert result == number
    assert isinstance(result, str)
```