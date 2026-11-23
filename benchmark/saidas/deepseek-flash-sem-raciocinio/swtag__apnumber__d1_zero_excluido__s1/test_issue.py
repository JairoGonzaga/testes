from alvo import apnumber


def test_apnumber_zero_is_word():
    assert apnumber(0) == "zero"


def test_apnumber_zero_float_is_word():
    assert apnumber(0.0) == "zero"


def test_apnumber_all_single_digits_are_words():
    words = (
        "zero", "one", "two", "three", "four",
        "five", "six", "seven", "eight", "nine",
    )
    for value, word in enumerate(words):
        assert apnumber(value) == word, f"apnumber({value}) should be {word!r}"


def test_apnumber_out_of_range_still_digits():
    assert apnumber(10) == "10"
    assert apnumber(-1) == "-1"
