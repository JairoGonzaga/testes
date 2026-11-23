from alvo import validate


def test_validate_returns_int_value_unchanged():
    number = 79927398713

    result = validate(number)

    assert result == number
    assert isinstance(result, int)


def test_validate_returns_valid_string_value_unchanged():
    number = "79927398713"

    result = validate(number)

    assert result == number
    assert isinstance(result, str)
