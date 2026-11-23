from alvo import naturalsize


def test_exactly_one_kilobyte_is_converted_to_kb():
    # Issue: naturalsize(1000) returned '1000 Bytes' instead of '1.0 kB'.
    assert naturalsize(1000) == "1.0 kB"


def test_exactly_one_kibibyte_is_converted_to_kib():
    # Same boundary bug in binary mode: 1024 bytes should become '1.0 KiB'.
    assert naturalsize(1024, binary=True) == "1.0 KiB"


def test_exactly_one_kibibyte_is_converted_in_gnu_mode():
    # Same boundary bug in GNU mode: 1024 bytes should become '1.0K'.
    assert naturalsize(1024, gnu=True) == "1.0K"


def test_values_below_one_kilobyte_stay_in_bytes():
    # Boundary guard: values strictly below the base keep the Bytes unit.
    assert naturalsize(999) == "999 Bytes"
