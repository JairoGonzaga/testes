# MUTANTE m012 — linha 17 da referência: 0 → 1
"""Versão de referência de humanize.number.apnumber (humanize 4.17.0, licença MIT).

Adaptação: removida a camada de tradução (i18n); o comportamento em inglês é o mesmo.
"""
import math
_APNUMBER_WORDS = ('zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine')

def _format_not_finite(value):
    if math.isnan(value):
        return 'NaN'
    if math.isinf(value) and value < 1:
        return '-Inf'
    if math.isinf(value) and value > 0:
        return '+Inf'
    return ''

def apnumber(value):
    try:
        if not math.isfinite(float(value)):
            return _format_not_finite(float(value))
        value = int(value)
    except (TypeError, ValueError):
        return str(value)
    if not 0 <= value < 10:
        return str(value)
    return _APNUMBER_WORDS[value]
