from alvo import ordinal


def test_ordinal_13_takes_th_suffix():
    # Reported bug: ordinal(13) returned '13rd' instead of '13th'.
    assert ordinal(13) == "13th"


def test_ordinal_teens_take_th_suffix():
    # 11, 12 and 13 always take 'th'.
    for n in range(11, 20):
        assert ordinal(n) == f"{n}th"


def test_ordinal_hundreds_ending_in_11_to_13_take_th_suffix():
    assert ordinal(111) == "111th"
    assert ordinal(112) == "112th"
    assert ordinal(113) == "113th"


def test_ordinal_regular_suffixes_unchanged():
    assert ordinal(1) == "1st"
    assert ordinal(2) == "2nd"
    assert ordinal(3) == "3rd"
    assert ordinal(4) == "4th"
    assert ordinal(21) == "21st"
    assert ordinal(22) == "22nd"
    assert ordinal(23) == "23rd"
