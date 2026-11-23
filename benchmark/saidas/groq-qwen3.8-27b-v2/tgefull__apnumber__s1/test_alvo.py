import math

from alvo import apnumber, _format_not_finite, _APNUMBER_WORDS


# ---- _format_not_finite ----

def test_format_not_finite_nan():
    assert _format_not_finite(float("nan")) == "NaN"


def test_format_not_finite_neg_inf():
    assert _format_not_finite(float("-inf")) == "-Inf"


def test_format_not_finite_pos_inf():
    assert _format_not_finite(float("inf")) == "+Inf"


def test_format_not_finite_finite_returns_empty():
    assert _format_not_finite(5.0) == ""


# ---- apnumber: numbers 0-9 spelled out ----

def test_apnumber_words_all_digits():
    for i in range(10):
        assert apnumber(i) == _APNUMBER_WORDS[i]


def test_apnumber_zero():
    assert apnumber(0) == "zero"


# ---- apnumber: floats that are integral ----

def test_apnumber_float_integral():
    assert apnumber(7.0) == "seven"
    assert apnumber(0.0) == "zero"


def test_apnumber_float_negative_integral():
    assert apnumber(-1.0) == "-1"


# ---- apnumber: out-of-range integers -> str ----

def test_apnumber_out_of_range():
    assert apnumber(10) == "10"
    assert apnumber(999) == "999"
    assert apnumber(-1) == "-1"
    assert apnumber(123456) == "123456"


# ---- apnumber: non-integer floats -> str of int(value) ----
# value = int(value) then range checked

def test_apnumber_float_truncated():
    # int(7.9) = 7
    assert apnumber(7.9) == "seven"
    # int(3.14) = 3
    assert apnumber(3.14) == "three"
    # int(9.9) = 9
    assert apnumber(9.9) == "nine"
    # int(0.5) = 0
    assert apnumber(0.5) == "zero"
    # int(-0.5) = 0
    assert apnumber(-0.5) == "zero"
    # int(12.9) = 12 -> out of range
    assert apnumber(12.9) == "12"


# ---- apnumber: NaN / Inf ----

def test_apnumber_nan():
    assert apnumber(float("nan")) == "NaN"


def test_apnumber_pos_inf():
    assert apnumber(float("inf")) == "+Inf"


def test_apnumber_neg_inf():
    assert apnumber(float("-inf")) == "-Inf"


# ---- apnumber: non-numeric input -> str(value) ----

def test_apnumber_string():
    assert apnumber("hello") == "hello"
    assert apnumber("") == ""


def test_apnumber_numeric_string():
    # float("5") = 5.0 is finite; int("5") = 5 -> "five"
    assert apnumber("5") == "five"
    # float("3.9") = 3.9 is finite, but int("3.9") raises ValueError -> "3.9"
    assert apnumber("3.9") == "3.9"
    # float("abc") raises ValueError -> "abc"
    assert apnumber("abc") == "abc"


def test_apnumber_list_raises_typeerror():
    # float([1]) raises TypeError -> str([1])
    assert apnumber([1]) == "[1]"


def test_apnumber_none():
    # float(None) raises TypeError -> str(None)
    assert apnumber(None) == "None"


# ---- apnumber: boolean ----
# bool is subclass of int: float(True)=1.0, int(True)=1
def test_apnumber_bool():
    assert apnumber(True) == "one"
    assert apnumber(False) == "zero"


# ---- apnumber: string that float parses but is out of range ----
def test_apnumber_numeric_string_out_of_range():
    # float("99") = 99.0, int("99") = 99 -> out of range
    assert apnumber("99") == "99"