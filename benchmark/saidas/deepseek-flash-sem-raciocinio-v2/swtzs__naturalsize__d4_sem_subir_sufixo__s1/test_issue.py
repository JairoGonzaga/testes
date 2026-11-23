from alvo import naturalsize


def test_naturalsize_rounds_up_to_next_unit():
    assert naturalsize(999999) == "1.0 MB"
