def test_decimal_and_binary_suffix_selection():
    assert naturalsize(1000) == "1.0 kB"
    assert naturalsize(1000, binary=True) == "1000 Bytes"
    assert naturalsize(1024, binary=True) == "1.0 KiB"
    assert naturalsize(1024) == "1.0 kB"
    assert naturalsize(1) == "1 Byte"
    assert naturalsize(0) == "0 Bytes"
    assert naturalsize(-1) == "-1 Byte"
    assert naturalsize(-1024) == "-1.0 kB"
