from alvo import naturalsize


def test_exact_kilobyte_is_converted():
    assert naturalsize(1000) == "1.0 kB"


def test_exact_kilobyte_binary():
    assert naturalsize(1024, binary=True) == "1.0 KiB"


def test_exact_kilobyte_gnu():
    assert naturalsize(1024, gnu=True) == "1.0K"


def test_just_below_kilobyte_still_bytes():
    assert naturalsize(999) == "999 Bytes"


def test_larger_values_unaffected():
    assert naturalsize(1000000) == "1.0 MB"
    assert naturalsize(1) == "1 Byte"
