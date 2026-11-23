import pytest

from alvo import InvalidFormat, validate


@pytest.mark.parametrize(
    "number",
    [
        "00000000000",
        "000.000.000-00",
    ],
)
def test_all_zeros_cpf_is_rejected_with_invalid_format(number):
    with pytest.raises(InvalidFormat):
        validate(number)


def test_valid_cpf_is_still_accepted():
    assert validate("52998224725") == "52998224725"
