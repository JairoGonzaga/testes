def test_c23_r2_fracao_fora_da_faixa_usa_inteiro_truncado():
    # [R2/fronteira]
    # Fora de 0..9 o retorno e o inteiro truncado, e nao a representacao do valor original.
    assert apnumber(10.7) == '10'
    assert apnumber(-2.5) == '-2'
    assert apnumber(1e3) == '1000'
