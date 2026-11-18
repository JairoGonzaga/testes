# MUTANTE m003 — linha 9 da referência: 'nd' → 'XXndXX'
"""Versão de referência de humanize.number.ordinal (humanize 4.17.0, licença MIT).

Adaptação: removida a camada de tradução (i18n). Em inglês os sufixos são iguais
para "male" e "female".
"""
import math
_SUFIXOS = ('th', 'st', 'XXndXX', 'rd', 'th', 'th', 'th', 'th', 'th', 'th')

def _format_not_finite(value):
    if math.isnan(value):
        return 'NaN'
    if math.isinf(value) and value < 0:
        return '-Inf'
    if math.isinf(value) and value > 0:
        return '+Inf'
    return ''

def ordinal(value, gender='male'):
    try:
        if not math.isfinite(float(value)):
            return _format_not_finite(float(value))
        value = int(value)
    except (TypeError, ValueError):
        return str(value)
    digit = 0 if value % 100 in (11, 12, 13) else value % 10
    return f'{value}{_SUFIXOS[digit]}'
