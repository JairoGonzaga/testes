# MUTANTE m008 — linha 9 da referência: 'PB' → 'XXPBXX'
"""Versão de referência de humanize.filesize.naturalsize (humanize 4.17.0, licença MIT).

Adaptação: removida a camada de tradução (i18n).
"""
from math import log
suffixes = {'decimal': ('kB', 'MB', 'GB', 'TB', 'XXPBXX', 'EB', 'ZB', 'YB', 'RB', 'QB'), 'binary': ('KiB', 'MiB', 'GiB', 'TiB', 'PiB', 'EiB', 'ZiB', 'YiB', 'RiB', 'QiB'), 'gnu': 'KMGTPEZYRQ'}

def naturalsize(value, binary=False, gnu=False, format='%.1f'):
    if gnu:
        suffix = suffixes['gnu']
    elif binary:
        suffix = suffixes['binary']
    else:
        suffix = suffixes['decimal']
    base = 1024 if gnu or binary else 1000
    bytes_ = float(value)
    abs_bytes = abs(bytes_)
    if abs_bytes == 1 and (not gnu):
        return '%d Byte' % int(bytes_)
    if abs_bytes < base:
        return f'{int(bytes_)}B' if gnu else '%d Bytes' % int(bytes_)
    exp = int(min(log(abs_bytes, base), len(suffix)))
    if exp < len(suffix) and abs(float(format % (abs_bytes / base ** exp))) >= base:
        exp += 1
    space = '' if gnu else ' '
    return format % (bytes_ / base ** exp) + space + suffix[exp - 1]
