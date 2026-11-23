def test_arredondamento_de_fronteira_com_formato_e_sinal():
    # A unidade so sobe quando o valor arredondado pelo formato chega a 1000,
    # o numero e reformatado com o mesmo formato, e nao ha subida acima de googol.
    assert intword(999949) == '999.9 thousand'
    assert intword(999999, '%.2f') == '1.00 million'
    assert intword(-999999, '%.2f') == '-1.00 million'
    assert intword(-999999999) == '-1.0 billion'
    assert intword(10**102 - 1) == '100.0 googol'
