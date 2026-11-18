# Este arquivo é copiado como conftest.py para a pasta temporária de cada execução do
# pytest. Ele NÃO é visto pelo modelo. Ele:
#   1. registra o resultado de cada teste (passou / falhou / erro) em JSON;
#   2. opcionalmente registra os argumentos de cada chamada à função-alvo (fronteiras);
#   3. opcionalmente roda só os testes válidos (para a cobertura de ramos).
import functools
import inspect
import json
import os

import pytest

_RESULTADOS = os.environ.get("AT_RESULTADOS")
_LOG = os.environ.get("AT_LOG_CHAMADAS")
_FUNCAO = os.environ.get("AT_FUNCAO")
_SO_VALIDOS = os.environ.get("AT_SO_VALIDOS")

_estado = {"teste": None, "resultados": {}, "mensagens": {}, "erros_coleta": [], "coletados": 0}

if _LOG and _FUNCAO:
    import alvo

    _original = getattr(alvo, _FUNCAO)
    try:
        _sig = inspect.signature(_original)
    except (TypeError, ValueError):
        _sig = None
    _arquivo_log = open(_LOG, "a", encoding="utf-8")

    @functools.wraps(_original)
    def _espiao(*args, **kwargs):
        try:
            ligacao = _sig.bind(*args, **kwargs)
            ligacao.apply_defaults()
            dados = dict(ligacao.arguments)
        except Exception:
            dados = {"_args": list(args), "_kwargs": kwargs}
        try:
            linha = json.dumps({"teste": _estado["teste"], "args": dados}, default=repr)
        except Exception:
            linha = json.dumps({"teste": _estado["teste"], "args": {"_repr": repr(dados)}})
        _arquivo_log.write(linha + "\n")
        _arquivo_log.flush()
        return _original(*args, **kwargs)

    setattr(alvo, _FUNCAO, _espiao)


def pytest_collection_modifyitems(config, items):
    if not _SO_VALIDOS:
        return
    with open(_SO_VALIDOS, encoding="utf-8") as f:
        validos = set(json.load(f))
    manter = [i for i in items if i.nodeid in validos]
    retirar = [i for i in items if i.nodeid not in validos]
    items[:] = manter
    if retirar:
        config.hook.pytest_deselected(items=retirar)


def pytest_collection_finish(session):
    _estado["coletados"] = len(session.items)


def pytest_collectreport(report):
    if report.failed:
        _estado["erros_coleta"].append({"nodeid": report.nodeid, "erro": str(report.longrepr)[-3000:]})


@pytest.hookimpl(tryfirst=True)
def pytest_runtest_setup(item):
    _estado["teste"] = item.nodeid


def pytest_runtest_logreport(report):
    r = _estado["resultados"]
    if report.when == "setup":
        if report.failed:
            r[report.nodeid] = "error"
        elif report.skipped:
            r[report.nodeid] = "skipped"
    elif report.when == "call":
        if report.passed:
            r[report.nodeid] = "passed"
        elif report.failed:
            r[report.nodeid] = "failed"
        else:
            r[report.nodeid] = "skipped"
    elif report.when == "teardown" and report.failed and r.get(report.nodeid) == "passed":
        r[report.nodeid] = "error"
    if report.failed:
        _estado["mensagens"][report.nodeid] = report.longreprtext[-800:]


def pytest_sessionfinish(session, exitstatus):
    if _RESULTADOS:
        with open(_RESULTADOS, "w", encoding="utf-8") as f:
            json.dump({k: v for k, v in _estado.items() if k != "teste"} | {"exitstatus": int(exitstatus)},
                      f, ensure_ascii=False, indent=1)
