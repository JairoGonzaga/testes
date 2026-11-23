def test_c28_r4_sufixo_errado_exaustivo():
    # [R4/invalida]
    base = '390533447'
    assert validate(base + '05') == '39053344705'
    for d1 in range(10):
        for d2 in range(10):
            sufixo = f'{d1}{d2}'
            if sufixo == '05':
                continue
            with pytest.raises(InvalidChecksum):
                validate(base + sufixo)
