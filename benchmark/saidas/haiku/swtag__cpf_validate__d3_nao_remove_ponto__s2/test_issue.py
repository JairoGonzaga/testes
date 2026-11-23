import pytest

from alvo import InvalidChecksum, validate


def test_formatted_cpf_with_dots_and_hyphen_is_accepted():
    # Issue: validate('111.444.777-35') raises InvalidFormat; expected '11144477735'.
    assert validate("111.444.777-35") == "11144477735"


def test_formatted_cpf_with_dots_only_is_accepted():
    # Dots are documented as removable separators, so the same CPF without
    # the hyphen should also validate to the compact form.
    assert validate("111.444.777.35") == "11144477735"


def test_formatted_cpf_with_dots_and_wrong_check_digits_raises_checksum_error():
    # A dotted CPF with an invalid verifier digit must be reported as a
    # checksum error, not as a format error.
    with pytest.raises(InvalidChecksum):
        validate("111.444.777-36")
