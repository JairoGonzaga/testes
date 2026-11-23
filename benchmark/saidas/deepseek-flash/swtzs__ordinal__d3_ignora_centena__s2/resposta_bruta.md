```python
import pytest

from alvo import ordinal


@pytest.mark.parametrize(
    "value, expected",
    [
        (11, "11th"),
        (12, "12th"),
        (13, "13th"),
        (111, "111th"),
        (112, "112th"),
        (113, "113th"),
        (211, "211th"),
        (212, "212th"),
        (213, "213th"),
        (311, "311th"),
        (411, "411th"),
        (511, "511th"),
        (1011, "1011th"),
        (1012, "1012th"),
        (1013, "1013th"),
        (1111, "1111th"),
        (1112, "1112th"),
        (1113, "1113th"),
    ],
)
def test_ordinal_uses_th_for_numbers_ending_in_11_12_13(value, expected):
    assert ordinal(value) == expected


@pytest.mark.parametrize(
    "value, expected",
    [
        (1, "1st"),
        (2, "2nd"),
        (3, "3rd"),
        (4, "4th"),
        (21, "21st"),
        (22, "22nd"),
        (23, "23rd"),
        (24, "24th"),
        (101, "101st"),
        (102, "102nd"),
        (103, "103rd"),
        (104, "104th"),
    ],
)
def test_ordinal_regular_suffixes_still_work(value, expected):
    assert ordinal(value) == expected
```