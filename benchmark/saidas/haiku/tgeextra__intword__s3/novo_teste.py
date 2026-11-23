def test_promocao_ate_decillion_com_sinal():
    # Logo abaixo de cada potência o valor arredonda para 1000 e deve subir
    # para a unidade seguinte; o sinal negativo também deve ser preservado.
    casos = [
        (10**12 - 1, '1.0 trillion'),
        (10**15 - 1, '1.0 quadrillion'),
        (10**18 - 1, '1.0 quintillion'),
        (10**21 - 1, '1.0 sextillion'),
        (10**24 - 1, '1.0 septillion'),
        (10**27 - 1, '1.0 octillion'),
        (10**30 - 1, '1.0 nonillion'),
        (10**33 - 1, '1.0 decillion'),
    ]
    for valor, esperado in casos:
        assert intword(valor) == esperado
        assert intword(-valor) == '-' + esperado
