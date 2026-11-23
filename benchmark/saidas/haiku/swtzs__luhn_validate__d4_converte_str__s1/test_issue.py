import pytest

from alvo import validate


@pytest.mark.parametrize("number", [79927398713, 18])
def test_validate_returns_the_int_it_received(number):
    result = validate(number)
    assert result == number


@pytest.mark.parametrize("number", [79927398713, 18])
def test_validate_returns_an_int_for_int_input(number):
    result = validate(number)
    assert isinstance(result, int)
