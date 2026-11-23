from alvo import naturalsize


def test_exactly_one_kilobyte_is_converted_to_kb():
    assert naturalsize(1000) == "1.0 kB"


def test_exactly_one_kilobyte_float_is_converted_to_kb():
    assert naturalsize(1000.0) == "1.0 kB"


def test_negative_one_kilobyte_is_converted_to_kb():
    assert naturalsize(-1000) == "-1.0 kB"


def test_values_below_one_kilobyte_stay_in_bytes():
    assert naturalsize(999) == "999 Bytes"
