```python
import pytest
from alvo import validate


@pytest.mark.parametrize(
    "number",
    [
        "79927398713",
        "4539578763621486",
        "4111111111111111",
    ],
)
def test_valid_luhn_numbers_are_accepted(number):
    assert validate(number) == number


def test_textbook_luhn_example_returns_input():
    assert validate("79927398713") == "79927398713"
```