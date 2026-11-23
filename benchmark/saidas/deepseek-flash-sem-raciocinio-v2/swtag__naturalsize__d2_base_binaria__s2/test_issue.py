from alvo import naturalsize


def test_binary_uses_1024_mibibytes():
    # From the issue: 3000000 / 1024**2 = 2.86... -> '2.9 MiB'
    assert naturalsize(3000000, binary=True) == "2.9 MiB"


def test_binary_uses_1024_exact_kibibytes():
    assert naturalsize(2048, binary=True) == "2.0 KiB"
    assert naturalsize(1024, binary=True) == "1.0 KiB"


def test_binary_uses_1024_partial_kibibytes():
    # 3000 / 1024 = 2.929 -> '2.9 KiB'
    assert naturalsize(3000, binary=True) == "2.9 KiB"
    assert naturalsize(1536, binary=True) == "1.5 KiB"


def test_binary_uses_1024_gibibytes():
    assert naturalsize(1024 ** 3, binary=True) == "1.0 GiB"


def test_binary_larger_value():
    # 123456789 / 1024**2 = 117.737... -> '117.7 MiB'
    assert naturalsize(123456789, binary=True) == "117.7 MiB"


def test_binary_falls_back_to_bytes_below_1024():
    assert naturalsize(500, binary=True) == "500 Bytes"


def test_decimal_still_uses_1000():
    assert naturalsize(3000000) == "3.0 MB"
