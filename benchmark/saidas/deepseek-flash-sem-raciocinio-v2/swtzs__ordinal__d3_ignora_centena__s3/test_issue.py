from alvo import ordinal


def test_ordinal_111_is_th():
    # Reported in the issue: ordinal(111) must be '111th'.
    assert ordinal(111) == "111th"


def test_ordinal_small_values_still_work():
    # Values stated as already correct in the issue / by the source table.
    assert ordinal(11) == "11th"
    assert ordinal(12) == "12th"
    assert ordinal(13) == "13th"
    assert ordinal(1) == "1st"
    assert ordinal(2) == "2nd"
    assert ordinal(3) == "3rd"
    assert ordinal(4) == "4th"
