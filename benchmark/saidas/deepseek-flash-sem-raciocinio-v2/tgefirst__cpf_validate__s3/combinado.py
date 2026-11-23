"""Testes de validate."""

import math

import pytest

from alvo import validate, ValidationError, InvalidFormat, InvalidLength, InvalidChecksum


def test_c1_r1():
    # [R1/normal]
    assert validate('390.533.447-05') == '39053344705'



from alvo import compact, clean, isdigits


def test_c1_r2_erros_e_auxiliares():
    # [R2/erros] comprimento errado, digito verificador errado e formato invalido
    with pytest.raises(InvalidLength):
        validate('3905334470')
    with pytest.raises(InvalidLength):
        validate('390533447051')
    with pytest.raises(InvalidChecksum):
        validate('39053344706')
    with pytest.raises(InvalidFormat):
        validate('00000000000')
    with pytest.raises(InvalidFormat):
        validate('3905334470a')
    with pytest.raises(InvalidFormat):
        validate(None)
    # InvalidLength e subclasse de InvalidFormat (que e subclasse de ValueError)
    assert issubclass(InvalidLength, InvalidFormat)
    assert issubclass(InvalidFormat, ValidationError)
    assert issubclass(ValidationError, ValueError)
    # separadores sao removidos por compact/clean
    assert compact(' 390.533.447-05 ') == '39053344705'
    assert clean('390-533', '-') == '390533'


def test_c1_r2_validos_auxiliares():
    # [R2/normal] outros formatos validos do mesmo numero
    assert validate('390 533 447 05') == '39053344705'
    assert validate(' 39053344705 ') == '39053344705'
    assert isdigits('123') is True
    assert isdigits('12a') is False
