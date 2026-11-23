def test_r3_string_with_spaces():
    # [R3/normal] - string com espaços, float() aceita ' 2 '
    assert apnumber(' 2 ') == 'two'