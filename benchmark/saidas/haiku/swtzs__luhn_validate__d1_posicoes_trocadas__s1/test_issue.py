import pytest

from alvo import InvalidChecksum, validate


@pytest.mark.parametrize(
    "number",
    [
        "79927398713",       # textbook Luhn example from the issue
        "4111111111111111",  # Visa test number
        "5555555555554444",  # MasterCard test number
        "378282246310005",   # Amex test number
        "6011111111111117",  # Discover test number
    ],
)
def test_valid_luhn_numbers_are_accepted(number):
    assert validate(number) == number


def test_issue_textbook_example_is_accepted():
    assert validate("79927398713") == "79927398713"


@pytest.mark.parametrize("number", ["79927398714", "79927398710"])
def test_invalid_luhn_numbers_are_rejected(number):
    with pytest.raises(InvalidChecksum):
        validate(number)
