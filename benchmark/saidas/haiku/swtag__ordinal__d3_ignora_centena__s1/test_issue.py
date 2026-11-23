import pytest

from alvo import ordinal


def _expected_ordinal(n):
    # English ordinal rule: 11, 12 and 13 (including when they are the last
    # two digits of a larger number, e.g. 111, 1012) take 'th'; otherwise the
    # last digit decides: 1 -> 'st', 2 -> 'nd', 3 -> 'rd', anything else 'th'.
    if n % 100 in (11, 12, 13):
        suffix = "th"
    else:
        suffix = {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")
    return f"{n}{suffix}"


@pytest.mark.parametrize(
    "value, expected",
    [
        (111, "111th"),
        (112, "112th"),
        (113, "113th"),
        (211, "211th"),
        (1011, "1011th"),
        (1012, "1012th"),
        (1013, "1013th"),
    ],
)
def test_ordinal_teens_suffix_for_larger_numbers(value, expected):
    assert ordinal(value) == expected


@pytest.mark.parametrize(
    "value, expected",
    [
        (1, "1st"),
        (2, "2nd"),
        (3, "3rd"),
        (4, "4th"),
        (11, "11th"),
        (12, "12th"),
        (13, "13th"),
        (21, "21st"),
        (101, "101st"),
        (102, "102nd"),
        (103, "103rd"),
        (110, "110th"),
        (121, "121st"),
    ],
)
def test_ordinal_small_and_regular_numbers(value, expected):
    assert ordinal(value) == expected


def test_ordinal_matches_reference_over_range():
    mismatches = [
        (n, ordinal(n))
        for n in range(1, 2000)
        if ordinal(n) != _expected_ordinal(n)
    ]
    assert mismatches == []
