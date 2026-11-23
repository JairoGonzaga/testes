def test_c34_r3_largest_ordinal_no_rounding_to_next():
    # [R3/fronteira] valor no maior ordinal (googol) nao deve tentar promover
    # para 'googol+1'; deve formatar normalmente.
    assert intword(15 * 10**100) == '15.0 googol'
