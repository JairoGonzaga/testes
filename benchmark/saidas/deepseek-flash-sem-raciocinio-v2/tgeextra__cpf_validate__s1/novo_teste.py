

def test_c28_r6_compact_strip_extremos():
    # [R6/fronteira] espaços e separadores nas extremidades, além de hífen isolado
    assert validate('  529.982.247-25  ') == '52998224725'
    assert validate('529982247- 25') == '52998224725'
    with pytest.raises(InvalidFormat):
        validate('   ')
