import pytest

from alvo import intword


def test_intword_exactly_one_thousand():
    """Exactly 1000 must be humanized (see ISSUE.md)."""
    assert intword(1000) == "1.0 thousand"


def test_intword_exactly_negative_one_thousand():
    """-1000 must be humanized too, with the sign preserved."""
    assert intword(-1000) == "-1.0 thousand"


def test_intword_one_thousand_float():
    """The same must hold when 1000 is passed as a float."""
    assert intword(1000.0) == "1.0 thousand"


def test_intword_one_thousand_string():
    """The same must hold when 1000 is passed as a string."""
    assert intword("1000") == "1.0 thousand"


@pytest.mark.parametrize(
    "value, expected",
    [
        (999, "999"),
        (1000, "1.0 thousand"),
        (1001, "1.0 thousand"),
        (1500, "1.5 thousand"),
        (1000000, "1.0 million"),
        (10 ** 9, "1.0 billion"),
        (-1000, "-1.0 thousand"),
        (-1500, "-1.5 thousand"),
    ],
)
def test_intword_boundaries(value, expected):
    """Behaviour around the thousand threshold is consistent at and above it."""
    assert intword(value) == expected


def test_intword_repeated_calls_are_stable():
    """Calling intword on 1000 repeatedly yields the humanized form each time."""
    results = {intword(1000) for _ in range(3)}
    assert results == {"1.0 thousand"}
