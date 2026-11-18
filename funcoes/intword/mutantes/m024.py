# MUTANTE m024 — linha 12 da referência: 'nonillion' → 'XXnonillionXX'
"""Versão de referência de humanize.number.intword (humanize 4.17.0, licença MIT).

Adaptação: removida a camada de tradução (i18n); separador decimal fixo em ".".
"""
import bisect
import math
powers = [10 ** x for x in (3, 6, 9, 12, 15, 18, 21, 24, 27, 30, 33, 100)]
human_powers = ('thousand', 'million', 'billion', 'trillion', 'quadrillion', 'quintillion', 'sextillion', 'septillion', 'octillion', 'XXnonillionXX', 'decillion', 'googol')

def _format_not_finite(value):
    if math.isnan(value):
        return 'NaN'
    if math.isinf(value) and value < 0:
        return '-Inf'
    if math.isinf(value) and value > 0:
        return '+Inf'
    return ''

def intword(value, format='%.1f'):
    try:
        if not math.isfinite(float(value)):
            return _format_not_finite(float(value))
        value = int(value)
    except (TypeError, ValueError):
        return str(value)
    if value < 0:
        value *= -1
        negative_prefix = '-'
    else:
        negative_prefix = ''
    if value < powers[0]:
        return f'{negative_prefix}{value}'
    ordinal = bisect.bisect_right(powers, value)
    largest_ordinal = ordinal == len(powers)
    ordinal -= 1
    power = powers[ordinal]
    chopped = value / power
    rounded_value = float(format % chopped)
    if not largest_ordinal and rounded_value == powers[ordinal + 1] // power:
        ordinal += 1
        rounded_value = 1.0
    unit = human_powers[ordinal]
    number = format % rounded_value
    return f'{negative_prefix}{number} {unit}'
