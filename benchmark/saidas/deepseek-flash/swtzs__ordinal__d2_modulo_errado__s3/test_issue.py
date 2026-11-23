from alvo import ordinal


def test_ordinal_eleven_has_th_suffix():
    assert ordinal(11) == "11th"
