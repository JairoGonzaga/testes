def test_c21_r4():
    # [R4/invalida] qualquer troca de um único símbolo em um número válido é detectada
    casos = [
        ('79927398713', '0123456789'),
        ('4111111111111111', '0123456789'),
        ('1a2b1', '0123456789abcdef'),
    ]
    for valido, alfabeto in casos:
        assert validate(valido, alphabet=alfabeto) == valido
        for pos, original in enumerate(valido):
            for novo in alfabeto:
                if novo == original:
                    continue
                trocado = valido[:pos] + novo + valido[pos + 1:]
                with pytest.raises(InvalidChecksum):
                    validate(trocado, alphabet=alfabeto)
