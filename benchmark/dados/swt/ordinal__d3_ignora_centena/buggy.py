import math

_SUFIXOS = ("th", "st", "nd", "rd", "th", "th", "th", "th", "th", "th")


def _format_not_finite(value):
    if math.isnan(value):
        return "NaN"
    if math.isinf(value) and value < 0:
        return "-Inf"
    if math.isinf(value) and value > 0:
        return "+Inf"
    return ""


def ordinal(value, gender="male"):
    try:
        if not math.isfinite(float(value)):
            return _format_not_finite(float(value))
        value = int(value)
    except (TypeError, ValueError):
        return str(value)
    digit = 0 if value in (11, 12, 13) else value % 10
    return f"{value}{_SUFIXOS[digit]}"
