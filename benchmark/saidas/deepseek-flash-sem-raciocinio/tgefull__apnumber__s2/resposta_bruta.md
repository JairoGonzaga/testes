```python
import math

import pytest

from alvo import (
    _APNUMBER_WORDS,
    _format_not_finite,
    apnumber,
)


class TestApnumberWords:
    @pytest.mark.parametrize(
        "value,expected",
        [
            (0, "zero"),
            (1, "one"),
            (2, "two"),
            (3, "three"),
            (4, "four"),
            (5, "five"),
            (6, "six"),
            (7, "seven"),
            (8, "eight"),
            (9, "nine"),
        ],
    )
    def test_int_words(self, value, expected):
        assert apnumber(value) == expected

    @pytest.mark.parametrize("value", range(10))
    def test_all_words_reachable(self, value):
        assert apnumber(value) == _APNUMBER_WORDS[value]

    def test_words_tuple_contents(self):
        assert _APNUMBER_WORDS == (
            "zero", "one", "two", "three", "four",
            "five", "six", "seven", "eight", "nine",
        )
        assert len(_APNUMBER_WORDS) == 10


class TestApnumberOutOfRange:
    @pytest.mark.parametrize(
        "value,expected",
        [
            (-1, "-1"),
            (-10, "-10"),
            (10, "10"),
            (11, "11"),
            (100, "100"),
            (1000, "1000"),
        ],
    )
    def test_out_of_range_returns_str(self, value, expected):
        assert apnumber(value) == expected

    def test_out_of_range_is_string(self):
        result = apnumber(10)
        assert isinstance(result, str)
        assert result == "10"


class TestApnumberFloats:
    @pytest.mark.parametrize(
        "value,expected",
        [
            (0.0, "zero"),
            (1.0, "one"),
            (9.0, "nine"),
            (1.4, "one"),
            (1.5, "one"),
            (1.9, "one"),
            (2.999, "two"),
            (0.99, "zero"),
            (-0.5, "zero"),
            (-0.99, "zero"),
        ],
    )
    def test_float_truncation(self, value, expected):
        assert apnumber(value) == expected

    @pytest.mark.parametrize(
        "value,expected",
        [
            (9.9, "nine"),
            (10.0, "10"),
            (10.5, "10"),
            (-1.1, "-1"),
            (-1.9, "-1"),
            (-2.0, "-2"),
        ],
    )
    def test_float_out_of_range_after_truncation(self, value, expected):
        assert apnumber(value) == expected


class TestApnumberBool:
    def test_true_is_one(self):
        assert apnumber(True) == "one"

    def test_false_is_zero(self):
        assert apnumber(False) == "zero"


class TestApnumberNumericStrings:
    @pytest.mark.parametrize(
        "value,expected",
        [
            ("0", "zero"),
            ("1", "one"),
            ("9", "nine"),
            ("5", "five"),
            ("1.9", "one"),
            ("2.5", "two"),
            ("10", "10"),
            ("-1", "-1"),
        ],
    )
    def test_numeric_strings(self, value, expected):
        assert apnumber(value) == expected

    def test_non_numeric_string(self):
        assert apnumber("abc") == "abc"

    def test_empty_string(self):
        assert apnumber("") == ""

    def test_whitespace_string(self):
        assert apnumber("   ") == "   "

    def test_string_nan(self):
        assert apnumber("nan") == "NaN"

    def test_string_inf(self):
        assert apnumber("inf") == "+Inf"

    def test_string_neg_inf(self):
        assert apnumber("-inf") == "-Inf"


class TestApnumberNonFinite:
    def test_float_nan(self):
        assert apnumber(float("nan")) == "NaN"

    def test_float_inf(self):
        assert apnumber(float("inf")) == "+Inf"

    def test_float_neg_inf(self):
        assert apnumber(float("-inf")) == "-Inf"

    def test_math_nan(self):
        assert apnumber(math.nan) == "NaN"

    def test_math_inf(self):
        assert apnumber(math.inf) == "+Inf"

    def test_math_neg_inf(self):
        assert apnumber(-math.inf) == "-Inf"


class TestApnumberErrors:
    def test_none(self):
        assert apnumber(None) == "None"

    def test_list(self):
        value = [1, 2, 3]
        assert apnumber(value) == str(value)

    def test_dict(self):
        value = {"a": 1}
        assert apnumber(value) == str(value)

    def test_object(self):
        class Foo:
            def __str__(self):
                return "foo!"

        assert apnumber(Foo()) == "foo!"

    def test_complex(self):
        value = 1 + 2j
        assert apnumber(value) == str(value)


class TestFormatNotFinite:
    def test_nan(self):
        assert _format_not_finite(float("nan")) == "NaN"

    def test_pos_inf(self):
        assert _format_not_finite(float("inf")) == "+Inf"

    def test_neg_inf(self):
        assert _format_not_finite(float("-inf")) == "-Inf"

    @pytest.mark.parametrize("value", [0.0, 1.0, -1.0, 1e300, -1e300])
    def test_finite_returns_empty(self, value):
        assert _format_not_finite(value) == ""

    def test_math_constants(self):
        assert _format_not_finite(math.nan) == "NaN"
        assert _format_not_finite(math.inf) == "+Inf"
        assert _format_not_finite(-math.inf) == "-Inf"


class TestReturnTypes:
    @pytest.mark.parametrize("value", [0, 5, 9, 10, -1, "abc", None])
    def test_always_returns_str(self, value):
        assert isinstance(apnumber(value), str)

    @pytest.mark.parametrize("value", [float("nan"), float("inf"), float("-inf")])
    def test_non_finite_returns_str(self, value):
        assert isinstance(apnumber(value), str)
```