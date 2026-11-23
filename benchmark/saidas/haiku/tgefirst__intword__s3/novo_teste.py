def test_intword_negativo_em_milhoes():
    # valor negativo: prefixo '-' e unidade pela magnitude do valor absoluto
    assert intword(-1500000) == '-1.5 million'
    assert intword(-999) == '-999'
