"""Leitura do conjunto de funções-alvo (pasta funcoes/)."""

import json
import re
from dataclasses import dataclass, field
from pathlib import Path

from . import config


@dataclass
class Funcao:
    pasta: Path
    nome: str                 # nome da pasta (ex.: cpf_validate)
    nome_funcao: str          # nome da função importada de alvo (ex.: validate)
    assinatura: str
    excecoes: list
    piloto: bool
    regras_md: str
    gabarito: dict
    meta: dict = field(default_factory=dict)

    # ---- caminhos ------------------------------------------------------------------
    @property
    def referencia(self) -> Path:
        return self.pasta / "referencia.py"

    @property
    def defeitos(self) -> list:
        return sorted((self.pasta / "defeitos").glob("*.py"))

    @property
    def pasta_mutantes(self) -> Path:
        return self.pasta / "mutantes"

    @property
    def mutantes(self) -> list:
        return sorted(self.pasta_mutantes.glob("m*.py"))

    @property
    def equivalentes(self) -> set:
        """Mutantes marcados à mão como equivalentes (um nome por linha, ex.: m007)."""
        arq = self.pasta_mutantes / "equivalentes.txt"
        if not arq.exists():
            return set()
        nomes = set()
        for linha in arq.read_text(encoding="utf-8").splitlines():
            linha = linha.split("#", 1)[0].strip()
            if linha:
                nomes.add(linha)
        return nomes

    # ---- informações para o prompt -------------------------------------------------
    @property
    def linha_importacao(self) -> str:
        nomes = [self.nome_funcao] + list(self.excecoes)
        return f"from alvo import {', '.join(nomes)}"

    @property
    def ids_regras(self) -> list:
        """IDs das regras como aparecem no regras.md (R1, R2…)."""
        ids = re.findall(r"^\s*[-*]\s*\**(R\d+)\**", self.regras_md, flags=re.M)
        return list(dict.fromkeys(ids))

    @property
    def regras_testaveis(self) -> list:
        return [r["id"] for r in self.gabarito.get("regras", []) if r.get("testavel", True)]


def carregar(nome: str) -> Funcao:
    pasta = config.PASTA_FUNCOES / nome
    meta = json.loads((pasta / "meta.json").read_text(encoding="utf-8"))
    gabarito_arq = pasta / "gabarito.json"
    gabarito = json.loads(gabarito_arq.read_text(encoding="utf-8")) if gabarito_arq.exists() else {}
    return Funcao(
        pasta=pasta,
        nome=nome,
        nome_funcao=meta["nome_funcao"],
        assinatura=meta["assinatura"],
        excecoes=meta.get("excecoes", []),
        piloto=bool(meta.get("piloto", False)),
        regras_md=(pasta / "regras.md").read_text(encoding="utf-8"),
        gabarito=gabarito,
        meta=meta,
    )


def listar(piloto: bool = False, nomes=None) -> list:
    """Funções da avaliação principal (piloto=False) ou do piloto (piloto=True)."""
    todas = sorted(p.name for p in config.PASTA_FUNCOES.iterdir() if (p / "meta.json").exists())
    if nomes:
        desconhecidas = set(nomes) - set(todas)
        if desconhecidas:
            raise SystemExit(f"Funções desconhecidas: {', '.join(sorted(desconhecidas))}")
        return [carregar(n) for n in nomes]
    return [f for f in (carregar(n) for n in todas) if f.piloto == piloto]
