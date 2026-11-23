from alvo import validate


def test_validate_returns_int_unchanged_for_valid_int():
    # Issue: validate(79927398713) returns '79927398713' instead of the int.
    assert validate(79927398713) == 79927398713


def test_validate_returns_int_type_for_valid_int():
    result = validate(79927398713)
    assert isinstance(result, int)
    assert not isinstance(result, str)


def test_validate_returns_int_unchanged_for_another_valid_int():
    assert validate(4111111111111111) == 4111111111111111
