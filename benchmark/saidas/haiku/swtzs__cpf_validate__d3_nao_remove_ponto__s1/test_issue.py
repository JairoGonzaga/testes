import pytest

from alvo import validate


def test_formatted_cpf_with_dots_is_accepted():
    # Issue example: dots and hyphen must be stripped before validating.
    assert validate('111.444.777-35') == '11144477735'


@pytest.mark.parametrize(
    "formatted, compact",
    [
        ("111.444.777-35", "11144477735"),
        ("529.982.247-25", "52998224725"),
    ],
)
def test_validate_returns_compact_form_for_dotted_cpf(formatted, compact):
    assert validate(formatted) == compact
