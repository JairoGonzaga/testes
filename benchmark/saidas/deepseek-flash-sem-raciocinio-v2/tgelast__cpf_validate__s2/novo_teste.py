

def test_c27_r7_normal_com_espacos():
    # [R7/normal]
    assert validate('  111.111.111-11  ') == '11111111111'


def test_c28_r7_retorno_compactado():
    # [R7/normal]
    assert validate(' 529 982 247 25 ') == '52998224725'
