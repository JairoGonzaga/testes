"""Reprodução do problema: CPF formatado com pontos é rejeitado por validate()."""

import pytest

from alvo import (
    compact,
    validate,
    isdigits,
    InvalidChecksum,
    InvalidFormat,
    InvalidLength,
)

VALID_CPF = "11144477735"
FORMATTED_CPF = "111.444.777-35"


def test_compact_removes_dots_and_hyphen():
    assert compact(FORMATTED_CPF) == VALID_CPF


def test_compact_strips_surrounding_whitespace_with_dots():
    assert compact("  " + FORMATTED_CPF + "  ") == VALID_CPF


def test_isdigits_on_compacted_formatted_cpf():
    assert isdigits(compact(FORMATTED_CPF))


def test_validate_accepts_formatted_cpf():
    assert validate(FORMATTED_CPF) == VALID_CPF


def test_validate_accepts_formatted_cpf_with_spaces():
    assert validate(" 111.444.777-35 ") == VALID_CPF


def test_validate_accepts_unformatted_cpf():
    assert validate(VALID_CPF) == VALID_CPF


def test_validate_formatted_cpf_with_bad_checksum_raises_checksum_error():
    # '111.444.777-36' tem dígito verificador inválido
    with pytest.raises(InvalidChecksum):
        validate("111.444.777-36")


def test_validate_formatted_cpf_with_wrong_length_raises_length_error():
    with pytest.raises(InvalidLength):
        validate("111.444.777-3")


def test_validate_rejects_non_digits():
    with pytest.raises(InvalidFormat):
        validate("111.444.777-3a")
