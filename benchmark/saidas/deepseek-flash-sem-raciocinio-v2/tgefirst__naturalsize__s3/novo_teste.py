

def test_c2_r1_bytes_e_escalas():
    # [R2/R3/valida]
    assert naturalsize(0) == "0 Bytes"
    assert naturalsize(1) == "1 Byte"
    assert naturalsize(-1) == "-1 Byte"
    assert naturalsize(999) == "999 Bytes"
    assert naturalsize(1000) == "1.0 kB"
    assert naturalsize(1500) == "1.5 kB"
    assert naturalsize(-2000) == "-2.0 kB"
    assert naturalsize(10**6) == "1.0 MB"
    assert naturalsize(1024) == "1.0 kB"
    assert naturalsize(10**24) == "1.0 YB"
    assert naturalsize(10**30) == "1.0 QB"
    assert naturalsize(10**33) == "1000.0 QB"


def test_c3_binario_gnu_e_formato():
    # [R2/R3]
    assert naturalsize(1024, binary=True) == "1.0 KiB"
    assert naturalsize(1024, gnu=True) == "1.0K"
    assert naturalsize(1, gnu=True) == "1B"
    assert naturalsize(1.9) == "1 Bytes"
    assert naturalsize(1500, format="%.0f") == "2 kB"
    assert naturalsize(1500, binary=True, format="%.2f") == "1.46 KiB"
