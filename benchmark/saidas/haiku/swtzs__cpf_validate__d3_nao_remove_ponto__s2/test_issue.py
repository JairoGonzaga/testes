import pytest

from alvo import validate, InvalidChecksum


def test_formatted_cpf_with_dots_and_hyphen_is_accepted():
    assert validate('111.444.777-35') == '11144477735'


@pytest.mark.parametrize(
    'formatted',
    [
        '111.444.777-35',
        '111 444 777 35',
        '111-444-777-35',
        '111.444.777 35',
        ' 111.444.777-35 ',
    ],
)
def test_formatted_valid_cpf_returns_compact_form(formatted):
    assert validate(formatted) == '11144477735'


def test_formatted_cpf_with_wrong_check_digits_raises_checksum_error():
    with pytest.raises(InvalidChecksum):
        validate('111.444.777-36')
