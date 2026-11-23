from alvo import naturalsize


def test_exactly_one_kilobyte_is_converted_to_kb():
    # Issue: naturalsize(1000) returned '1000 Bytes' instead of '1.0 kB'.
    assert naturalsize(1000) == "1.0 kB"


def test_just_below_one_kilobyte_stays_in_bytes():
    assert naturalsize(999) == "999 Bytes"


def test_just_above_one_kilobyte_is_converted_to_kb():
    assert naturalsize(1001) == "1.0 kB"


def test_one_byte_keeps_singular_form():
    assert naturalsize(1) == "1 Byte"
