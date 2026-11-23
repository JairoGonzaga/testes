

def test_c34_r3_r5_r6():
    # [R3/fronteira] arredondamento promove para a proxima potencia
    assert intword(999999999999) == '1.0 trillion'
    # [R5/normal] formato inteiro com valor negativo grande
    assert intword(-1234000, '%0.3f') == '-1.234 million'
    # [R6/normal] inteiro grande com formato '%d'
    assert intword(123456789123456789, '%d') == '123 quadrillion'
    # [R3/normal] acima do googol em duas ordens de grandeza
    assert intword(10**102) == '100.0 googol'
    # [R2/normal] abaixo do googol mas na casa dos decilhoes
    assert intword(1500000000000000000000000000000000) == '1.5 decillion'
