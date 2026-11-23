

def test_c45_r7_arredondamento_promove_unidade():
    # [R7/fronteira] arredondamento do format empurra para a unidade seguinte
    assert naturalsize(1050, format='%.0f') == '1 kB'
    assert naturalsize(999, format='%.0f') == '999 Bytes'


def test_c46_r4_limite_superior_sufixos():
    # [R4/fronteira] exp limitado ao tamanho da lista de sufixos
    assert naturalsize(10**30) == '1.0 QB'
    assert naturalsize(10**33) == '1000.0 QB'


def test_c47_r6_gnu_nao_arredonda_e_base_grande():
    # [R6/normal] gnu com valor >= base de 1024
    assert naturalsize(1000, gnu=True) == '1000B'
    assert naturalsize(10**6, gnu=True) == '976.6K'
