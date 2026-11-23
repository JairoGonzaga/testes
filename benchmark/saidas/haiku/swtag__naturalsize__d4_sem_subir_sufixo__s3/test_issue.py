from alvo import naturalsize


def test_rounding_up_to_next_unit_promotes_unit():
    # naturalsize(999999) used to return '1000.0 kB'; the value rounds up to
    # 1000 kB, so the unit must be promoted to MB.
    assert naturalsize(999999) == "1.0 MB"


def test_rounding_up_to_next_unit_promotes_unit_for_gigabytes():
    # Same bug one unit higher: '1000.0 MB' must become '1.0 GB'.
    assert naturalsize(999999999) == "1.0 GB"


def test_values_that_do_not_round_up_keep_their_unit():
    assert naturalsize(999) == "999 Bytes"
    assert naturalsize(1000) == "1.0 kB"
    assert naturalsize(999000) == "999.0 kB"
