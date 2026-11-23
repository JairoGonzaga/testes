from alvo import validate


def test_validate_int_returns_int():
    number = 79927398713
    result = validate(number)
    assert result == 79927398713
    assert isinstance(result, int)


def test_validate_string_returns_string_unchanged():
    result = validate("79927398713")
    assert result == "79927398713"
    assert isinstance(result, str)
