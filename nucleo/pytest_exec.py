"""Roda um arquivo de testes contra uma versão da função, em uma pasta temporária isolada.

A versão (referência, defeituosa ou mutante) é copiada como `alvo.py`, de modo que o
mesmo arquivo de testes (`from alvo import ...`) roda sem alteração contra qualquer versão.
"""

import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from . import config

PLUGIN = Path(__file__).with_name("plugin_conftest.py")


def rodar_pytest(arquivo_teste: Path, arquivo_alvo: Path, nome_funcao: str,
                 registrar_chamadas=False, so_validos=None, cobertura=False,
                 junit: Path = None, timeout=None) -> dict:
    timeout = timeout or config.TIMEOUT_PYTEST_S
    with tempfile.TemporaryDirectory(prefix="agente_testes_") as tmp:
        tmp = Path(tmp)
        shutil.copy(arquivo_teste, tmp / "test_gerado.py")
        shutil.copy(arquivo_alvo, tmp / "alvo.py")
        shutil.copy(PLUGIN, tmp / "conftest.py")
        (tmp / "pytest.ini").write_text("[pytest]\n", encoding="utf-8")

        env = dict(os.environ)
        env.update({"AT_RESULTADOS": str(tmp / "resultados.json"), "PYTHONDONTWRITEBYTECODE": "1",
                    "PYTHONHASHSEED": "0", "AT_FUNCAO": nome_funcao})
        env.pop("AT_LOG_CHAMADAS", None)
        env.pop("AT_SO_VALIDOS", None)
        if registrar_chamadas:
            env["AT_LOG_CHAMADAS"] = str(tmp / "chamadas.jsonl")
        if so_validos is not None:
            (tmp / "validos.json").write_text(json.dumps(list(so_validos)), encoding="utf-8")
            env["AT_SO_VALIDOS"] = str(tmp / "validos.json")

        cmd = [sys.executable, "-m", "pytest", "test_gerado.py", "-q", "-p", "no:cacheprovider",
               "--rootdir", str(tmp), "-c", str(tmp / "pytest.ini"), "--no-header", "-rN"]
        if cobertura:
            cmd += ["--cov=alvo", "--cov-branch", f"--cov-report=json:{tmp / 'cov.json'}"]
        if junit:
            cmd += [f"--junitxml={tmp / 'junit.xml'}"]

        saida = {"timeout": False, "resultados": {}, "mensagens": {}, "erros_coleta": [],
                 "coletados": 0, "chamadas": [], "cobertura": None}
        try:
            proc = subprocess.run(cmd, cwd=tmp, env=env, capture_output=True, text=True,
                                  timeout=timeout, encoding="utf-8", errors="replace")
            saida["stdout"] = proc.stdout[-4000:]
            saida["codigo_saida"] = proc.returncode
        except subprocess.TimeoutExpired:
            saida["timeout"] = True
            return saida

        arq = tmp / "resultados.json"
        if arq.exists():
            saida.update(json.loads(arq.read_text(encoding="utf-8")))
        elif proc.returncode != 0:
            # pytest morreu antes de terminar (ex.: erro ao importar o conftest/alvo)
            saida["erros_coleta"].append({"nodeid": "", "erro": (proc.stdout + proc.stderr)[-3000:]})

        if registrar_chamadas and (tmp / "chamadas.jsonl").exists():
            for linha in (tmp / "chamadas.jsonl").read_text(encoding="utf-8").splitlines():
                try:
                    saida["chamadas"].append(json.loads(linha))
                except json.JSONDecodeError:
                    pass
        if cobertura and (tmp / "cov.json").exists():
            dados = json.loads((tmp / "cov.json").read_text(encoding="utf-8"))
            arquivos = dados.get("files", {})
            info = next((v for k, v in arquivos.items() if Path(k).name == "alvo.py"), None)
            if info:
                saida["cobertura"] = info["summary"]
        if junit and (tmp / "junit.xml").exists():
            Path(junit).parent.mkdir(parents=True, exist_ok=True)
            shutil.copy(tmp / "junit.xml", junit)
        return saida
