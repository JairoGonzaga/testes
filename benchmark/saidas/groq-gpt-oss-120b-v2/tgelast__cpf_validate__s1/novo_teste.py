def test_c27_hyphen_ignored():
    # Leading hyphen should be removed like any other deletechar and the number validated.
    assert validate('-123.456.789-09') == '12345678909'
