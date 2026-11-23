"""Reproducao do issue: validate() aceita o CPF todo de zeros.

Um CPF composto apenas por zeros nao e um numero valido e deve ser
rejeitado com InvalidFormat.
"""

import pytest

from alvo import (
    InvalidFormat,
    ValidationError,
    validate,
)


ZERO_CPF = "00000000000"


def test_all_zeros_cpf_is_rejected():
    """CPF 00000000000 deve ser rejeitado com InvalidFormat."""
    with pytest.raises(InvalidFormat):
        validate(ZERO_CPF)


def test_all_zeros_cpf_is_rejected_not_only_with_formatting():
    """A rejeicao deve acontecer tambem apos a compactacao do numero."""
    for value in ("000.000.000-00", "000 000 000 00", "000-000-000.00"):
        with pytest.raises(InvalidFormat):
            validate(value)


def test_all_zeros_cpf_raises_validation_error():
    """A excecao levantada deve ser um ValidationError (formato invalido)."""
    with pytest.raises(ValidationError):
        validate(ZERO_CPF)


def test_valid_cpf_still_accepted():
    """Garante que a correcao nao rejeita CPFs validos."""
    assert validate("11144477735") == "11144477735"
    assert validate("111.444.777-35") == "11144477735"
    assert validate("529.982.247-25") == "52998224725"


def test_invalid_checksum_still_rejected():
    """Digito verificador errado continua a levantar InvalidChecksum."""
    from alvo import InvalidChecksum

    with pytest.raises(InvalidChecksum):
        validate("111.444.777-36")


def test_invalid_length_still_rejected():
    """Comprimento errado continua a levantar InvalidLength."""
    from alvo import InvalidLength

    with pytest.raises(InvalidLength):
        validate("1234567890")


def test_non_digits_still_rejected():
    """Caracteres invalidos continuam a levantar InvalidFormat."""
    with pytest.raises(InvalidFormat):
        validate("111.444.777-3X")
