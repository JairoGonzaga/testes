import pytest

from alvo import validate


def test_issue_textbook_luhn_example_is_accepted():
    # 79927398713 has a valid Luhn check digit, so validate must return it.
    assert validate("79927398713") == "79927398713"


@pytest.mark.parametrize(
    "number",
    [
        "18",
        "4111111111111111",
        "4012888888881881",
        "378282246310005",
        "5105105105105100",
    ],
)
def test_other_valid_luhn_numbers_are_accepted(number):
    assert validate(number) == number
