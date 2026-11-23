import pytest

from alvo import InvalidChecksum, compact, validate


def test_validate_accepts_formatted_cpf_with_dots_and_hyphen():
    # '111.444.777-35' is a valid CPF in the usual XXX.XXX.XXX-XX format;
    # validate() must strip dots, spaces and hyphens and return the compact form.
    assert validate("111.444.777-35") == "11144477735"


def test_compact_removes_dots_spaces_and_hyphens():
    assert compact("111.444.777-35") == "11144477735"


def test_validate_dotted_cpf_with_wrong_check_digits_raises_checksum_error():
    # Same CPF with a wrong check digit must be reported as a checksum error,
    # not as a format error caused by the dots.
    with pytest.raises(InvalidChecksum):
        validate("111.444.777-36")
