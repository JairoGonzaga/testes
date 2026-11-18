# MUTANTE m004 — linha 22 da referência: * → /
"""Versão de referência de stdnum.luhn.validate (python-stdnum 2.2, licença LGPL-2.1+).

Adaptação: as exceções de stdnum foram copiadas para este arquivo.
"""

class ValidationError(ValueError):
    """Erro de validação genérico."""

class InvalidFormat(ValidationError):
    """Formato inválido."""

class InvalidChecksum(ValidationError):
    """Soma de verificação não confere."""

def checksum(number, alphabet='0123456789'):
    n = len(alphabet)
    values = tuple((alphabet.index(i) for i in reversed(str(number))))
    return (sum(values[::2]) + sum((sum(divmod(i / 2, n)) for i in values[1::2]))) % n

def validate(number, alphabet='0123456789'):
    if not bool(number):
        raise InvalidFormat()
    try:
        valid = checksum(number, alphabet) == 0
    except Exception:
        raise InvalidFormat()
    if not valid:
        raise InvalidChecksum()
    return number
