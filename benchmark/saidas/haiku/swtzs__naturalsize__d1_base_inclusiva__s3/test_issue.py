from alvo import naturalsize


def test_one_kilobyte_is_converted_to_kb():
    assert naturalsize(1000) == "1.0 kB"


def test_one_kilobyte_float_input_is_converted_to_kb():
    assert naturalsize(1000.0) == "1.0 kB"


def test_negative_one_kilobyte_is_converted_to_kb():
    assert naturalsize(-1000) == "-1.0 kB"


def test_one_kibibyte_in_binary_mode_is_converted_to_kib():
    assert naturalsize(1024, binary=True) == "1.0 KiB"


def test_value_below_one_kilobyte_stays_in_bytes():
    assert naturalsize(999) == "999 Bytes"


def test_value_just_above_one_kilobyte_is_converted_to_kb():
    assert naturalsize(1001) == "1.0 kB"
