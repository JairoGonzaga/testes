def test_c1_r2():
    # [R2/bytes]
    assert naturalsize(0) == "0 Bytes"
    assert naturalsize(1) == "1 Byte"
    assert naturalsize(2) == "2 Bytes"
    assert naturalsize(999) == "999 Bytes"
    assert naturalsize(1000) == "1.0 kB"
    assert naturalsize(1500) == "1.5 kB"
