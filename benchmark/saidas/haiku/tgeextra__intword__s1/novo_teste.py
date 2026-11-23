def test_c34_r3_transbordo_com_sinal_e_formato():
    # [R3/fronteira]
    # arredondamento que transborda para a potência seguinte mantém sinal e formato
    assert intword(-999999) == '-1.0 million'
    assert intword(999999, '%.2f') == '1.00 million'
    assert intword(10**33 - 1) == '1.0 decillion'
    assert intword(-(10**33 - 1), '%.0f') == '-1 decillion'
