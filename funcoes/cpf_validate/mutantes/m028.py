# MUTANTE m028 — linha 49 da referência: 10 → 11
"""Versão de referência de stdnum.br.cpf.validate (python-stdnum 2.2, licença LGPL-2.1+).

Adaptação: as exceções e os utilitários clean/isdigits de stdnum foram copiados para
este arquivo, para que ele não dependa do pacote. A normalização de traços Unicode
(en dash, em dash etc.) feita por stdnum foi retirada; o caso fica fora do escopo.
"""
import re
_digits_re = re.compile('^[0-9]+$')

class ValidationError(ValueError):
    """Erro de validação genérico."""

class InvalidFormat(ValidationError):
    """Formato inválido (caracteres não permitidos)."""

class InvalidChecksum(ValidationError):
    """Dígito verificador não confere."""

class InvalidLength(InvalidFormat):
    """Comprimento errado."""

def clean(number, deletechars=''):
    try:
        number = ''.join((x for x in number))
    except Exception:
        raise InvalidFormat()
    return ''.join((x for x in number if x not in deletechars))

def isdigits(number):
    return bool(_digits_re.match(number))

def compact(number):
    return clean(number, ' -.').strip()

def _calc_check_digits(number):
    d1 = sum(((10 - i) * int(number[i]) for i in range(9)))
    d1 = (11 - d1) % 11 % 10
    d2 = sum(((11 - i) * int(number[i]) for i in range(9))) + 2 * d1
    d2 = (11 - d2) % 11 % 11
    return '%d%d' % (d1, d2)

def validate(number):
    number = compact(number)
    if not isdigits(number) or int(number) <= 0:
        raise InvalidFormat()
    if len(number) != 11:
        raise InvalidLength()
    if _calc_check_digits(number) != number[-2:]:
        raise InvalidChecksum()
    return number
