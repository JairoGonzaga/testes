from alvo import ordinal


def test_eleven_is_th():
    # Expected value quoted directly from the issue report.
    assert ordinal(11) == "11th"


def test_teen_numbers_are_th():
    # Expected values obtained by tracing the code line by line; they share
    # the same faulty `value % 10 in (11, 12, 13)` predicate as the issue,
    # so they fail now and pass after the minimal fix.
    assert ordinal(12) == "12th"
    assert ordinal(13) == "13th"
