def test_c21_r4_digito_verificador_unico():
    # [R4/propriedade]
    casos = [
        ('0123456789', '7992739871', '3'),
        ('0123456789abcdef', '1a2b', '1'),
        ('01', '1', '1'),
        ('abc', 'bc', 'a'),
    ]
    for alfabeto, carga, esperado in casos:
        aceitos = []
        for digito in alfabeto:
            try:
                validate(carga + digito, alphabet=alfabeto)
            except InvalidChecksum:
                continue
            aceitos.append(digito)
        assert aceitos == [esperado]
