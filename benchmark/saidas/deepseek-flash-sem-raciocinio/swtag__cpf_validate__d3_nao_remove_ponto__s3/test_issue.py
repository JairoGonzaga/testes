import pytest

from alvo import validate, compact, ValidationError, InvalidFormat


def test_validate_formatted_cpf_with_dots():
    assert validate('111.444.777-35') == '11144477735'


def test_validate_formatted_cpf_with_spaces():
    assert validate('111 444 777 35') == '11144477735'


def test_compact_removes_dots_spaces_hyphens():
    assert compact('111.444.777-35') == '11144477735'


def test_validate_plain_cpf_still_works():
    assert validate('11144477735') == '11144477735'


def test_validate_invalid_checksum_formatted():
    with pytest.raises(ValidationError):
        validate('111.444.777-36')
