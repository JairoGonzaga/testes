def test_c2_r1():
    # [R1/normal] número sem pontuação também é aceito
    assert validate('39053344705') == '39053344705'
