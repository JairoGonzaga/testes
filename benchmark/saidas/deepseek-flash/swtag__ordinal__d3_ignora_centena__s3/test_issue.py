import pytest

from alvo import ordinal


@pytest.mark.parametrize(
    "value, expected",
    [
        (111, "111th"),
        (112, "112th"),
        (113, "113th"),
        (211, "211th"),
        (212, "212th"),
        (213, "213th"),
        (1011, "1011th"),
        (1012, "1012th"),
        (1013, "1013th"),
        (99111, "99111th"),
    ],
)
def test_teen_endings_use_th(value, expected):
    assert ordinal(value) == expected


@pytest.mark.parametrize(
    "value, expected",
    [
        (11, "11th"),
        (12, "12th"),
        (13, "13th"),
        (1, "1st"),
        (2, "2nd"),
        (3, "3rd"),
        (4, "4th"),
        (10, "10th"),
        (21, "21st"),
        (22, "22nd"),
        (23, "23rd"),
        (101, "101st"),
        (114, "114th"),
        (121, "121st"),
    ],
)
def test_basic_ordinals_still_correct(value, expected):
    assert ordinal(value) == expected
