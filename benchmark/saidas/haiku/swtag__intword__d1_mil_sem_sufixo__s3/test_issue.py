import pytest

from alvo import intword


def test_intword_exactly_one_thousand_is_humanized():
    # Reported bug: intword(1000) returned '1000' instead of '1.0 thousand'.
    assert intword(1000) == "1.0 thousand"


def test_intword_negative_exactly_one_thousand_is_humanized():
    # Same boundary, negative sign: magnitude 1000 must get the word suffix.
    assert intword(-1000) == "-1.0 thousand"


@pytest.mark.parametrize("value", [0, 1, 999, -999])
def test_intword_below_one_thousand_is_unchanged(value):
    assert intword(value) == str(value)


@pytest.mark.parametrize(
    "value, expected",
    [
        (1001, "1.0 thousand"),
        (1000000, "1.0 million"),
    ],
)
def test_intword_above_one_thousand_is_humanized(value, expected):
    assert intword(value) == expected
