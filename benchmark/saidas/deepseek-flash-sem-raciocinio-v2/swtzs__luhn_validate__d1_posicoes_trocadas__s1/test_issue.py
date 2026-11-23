from alvo import validate


def test_validate_accepts_textbook_luhn_number():
    # Issue states: 79927398713 has a valid Luhn check digit.
    # Expected: validate returns '79927398713'.
    assert validate("79927398713") == "79927398713"
