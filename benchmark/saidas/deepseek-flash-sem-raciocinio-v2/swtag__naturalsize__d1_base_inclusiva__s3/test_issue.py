from alvo import naturalsize


def test_exactly_one_kilobyte_decimal():
    assert naturalsize(1000) == "1.0 kB"


def test_exactly_one_kilobyte_negative():
    assert naturalsize(-1000) == "-1.0 kB"


def test_exactly_one_kibibyte_binary():
    assert naturalsize(1024, binary=True) == "1.0 KiB"


def test_one_kib_gnu():
    assert naturalsize(1024, gnu=True) == "1.0K"


def test_below_threshold_still_bytes():
    assert naturalsize(999) == "999 Bytes"
    assert naturalsize(1) == "1 Byte"
