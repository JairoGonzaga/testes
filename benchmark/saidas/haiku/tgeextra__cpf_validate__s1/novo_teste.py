def test_digito_resto_10_vira_zero():
    # Resto 10 (modulo 11) no calculo de cada digito verificador deve virar 0 (modulo 10).
    # Caso do 1o digito verificador (d1 = 0):
    assert validate('00000000604') == '00000000604'
    # Caso do 2o digito verificador (d2 = 0):
    assert validate('60000000060') == '60000000060'
