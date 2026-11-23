import pytest

from alvo import validate, InvalidChecksum


def test_wellknown_valid_cpf_11144477735_is_accepted():
    try:
        result = validate('11144477735')
    except InvalidChecksum as exc:
        pytest.fail("validate('11144477735') raised InvalidChecksum: %r" % (exc,))
    assert result == '11144477735'
