from alvo import apnumber


def test_nine_is_spelled_out():
    assert apnumber(9) == "nine"


def test_one_through_nine_are_spelled_out():
    expected = {
        1: "one",
        2: "two",
        3: "three",
        4: "four",
        5: "five",
        6: "six",
        7: "seven",
        8: "eight",
        9: "nine",
    }
    for number, word in expected.items():
        assert apnumber(number) == word, number


def test_numbers_of_ten_and_above_are_returned_as_digits():
    assert apnumber(10) == "10"
    assert apnumber(42) == "42"
