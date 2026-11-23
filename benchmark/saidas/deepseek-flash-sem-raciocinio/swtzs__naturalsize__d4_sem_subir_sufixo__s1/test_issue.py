import pytest
from alvo import naturalsize


def test_naturalsize_999999_promotes_to_megabytes():
    assert naturalsize(999999) == "1.0 MB"


def test_naturalsize_999999_binary_promotes_to_mebibytes():
    assert naturalsize(999999, binary=True) == "1.0 MiB"


def test_naturalsize_999999_gnu_promotes_to_megabytes():
    assert naturalsize(999999, gnu=True) == "1.0M"


def test_naturalsize_rounding_edge_stays_within_unit():
    result = naturalsize(999999)
    assert result.endswith("MB")
