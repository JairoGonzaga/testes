"""Funções auxiliares usadas nos critérios de fronteira do gabarito.

Cada fronteira do gabarito tem um "criterio": uma expressão Python avaliada sobre os
argumentos de cada chamada à função (com os valores padrão já preenchidos). Exemplo:

    "criterio": "eq(value, 1024) and binary and not gnu"

A fronteira conta como exercitada se ALGUM teste válido chamou a função com argumentos
que satisfazem o critério.
"""

import math


def eq(a, b) -> bool:
    """Igualdade estrita: True não é igual a 1 e "10" não é igual a 10."""
    if isinstance(a, bool) or isinstance(b, bool):
        return type(a) is type(b) and a == b
    if isinstance(a, str) or isinstance(b, str):
        return isinstance(a, str) and isinstance(b, str) and a == b
    try:
        return bool(a == b)
    except Exception:
        return False


def compacto(x):
    """Remove espaços, hífens e pontos (como a compactação do CPF). None se não for str."""
    if not isinstance(x, str):
        return None
    return "".join(c for c in x if c not in " -.").strip()


def qtd_digitos(x):
    """Quantidade de dígitos depois de compactar, se só restarem dígitos 0-9; senão None."""
    c = compacto(x)
    if c and c.isascii() and c.isdigit():
        return len(c)
    return None


def eh_zero(x) -> bool:
    c = compacto(x)
    return bool(c) and c.isascii() and c.isdigit() and int(c) == 0


def todos_iguais(x) -> bool:
    """11 dígitos iguais, diferentes de zero (ex.: 111.111.111-11)."""
    c = compacto(x)
    return bool(c) and len(c) == 11 and c.isascii() and c.isdigit() and len(set(c)) == 1 and c[0] != "0"


def dobro_ultrapassa(number, alphabet="0123456789") -> bool:
    """Luhn: existe caractere em posição par (da direita) cujo dobro é >= len(alphabet)?"""
    try:
        s = str(number)[::-1]
        n = len(alphabet)
        return any(2 * alphabet.index(c) >= n for c in s[1::2])
    except Exception:
        return False


AJUDANTES = {
    "eq": eq,
    "compacto": compacto,
    "qtd_digitos": qtd_digitos,
    "eh_zero": eh_zero,
    "todos_iguais": todos_iguais,
    "dobro_ultrapassa": dobro_ultrapassa,
    "math": math,
}

_BUILTINS = {"len": len, "isinstance": isinstance, "str": str, "int": int, "float": float,
             "abs": abs, "any": any, "all": all, "set": set, "bool": bool}


def satisfaz(criterio: str, argumentos: dict) -> bool:
    try:
        return bool(eval(criterio, {"__builtins__": _BUILTINS, **AJUDANTES}, dict(argumentos)))
    except Exception:
        return False
