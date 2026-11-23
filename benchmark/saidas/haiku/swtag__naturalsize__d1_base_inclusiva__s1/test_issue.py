from alvo import naturalsize


def test_exactly_one_kilobyte_is_converted_to_kb():
    # Reported bug: naturalsize(1000) returned '1000 Bytes' instead of '1.0 kB'.
    assert naturalsize(1000) == "1.0 kB"


def test_exactly_one_kibibyte_is_converted_to_kib():
    # Same boundary in binary mode (base 1024).
    assert naturalsize(1024, binary=True) == "1.0 KiB"


def test_exactly_one_kilobyte_gnu_is_converted():
    # Same boundary in gnu mode (base 1024, single-letter suffix).
    assert naturalsize(1024, gnu=True) == "1.0K"


def test_negative_exactly_one_kilobyte_is_converted():
    assert naturalsize(-1000) == "-1.0 kB"


def test_values_below_one_kilobyte_stay_in_bytes():
    assert naturalsize(999) == "999 Bytes"
    assert naturalsize(1000, binary=True) == "1000 Bytes"
