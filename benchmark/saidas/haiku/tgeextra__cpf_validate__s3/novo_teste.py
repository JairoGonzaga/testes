def test_c28_r1():
    # [R1/fronteira]
    # tab e quebra de linha nas bordas são removidos por strip()
    assert validate('\t390.533.447-05\n') == '39053344705'
    # tab no meio do número não é removido: formato inválido
    with pytest.raises(InvalidFormat):
        validate('390\t533447-05')
