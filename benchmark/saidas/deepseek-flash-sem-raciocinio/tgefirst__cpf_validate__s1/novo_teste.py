def test_c1_r2():
    # [R2/limite] números com 11 dígitos e DV válido calculado dinamicamente
    from alvo import _calc_check_digits
    base = '123456789'
    dv = _calc_check_digits(base + '00'[:0] or base)
    number = base + dv
    assert validate(number) == number
