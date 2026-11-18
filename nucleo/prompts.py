"""Prompts das duas condições. CONGELE este arquivo depois do piloto.

As duas condições recebem exatamente o mesmo contexto (regras, assinatura, importação e
o que se espera dos testes). Muda só o formato da resposta: A devolve código pytest;
B devolve um plano de casos em JSON, que o programa transforma em testes.
"""

SISTEMA = ("Você é um engenheiro de testes de software experiente. Você escreve testes "
           "unitários em Python com pytest a partir de especificações de regras de negócio.")


def contexto_comum(funcao) -> str:
    excecoes = ""
    if funcao.excecoes:
        excecoes = f"\nExceções que podem ser importadas de `alvo`: {', '.join(funcao.excecoes)}."
    return f"""Você vai criar testes unitários para a função descrita abaixo.
Você NÃO tem acesso ao código da função: baseie-se apenas nas regras de negócio.

## Assinatura
```python
{funcao.assinatura}
```

## Como importar
```python
{funcao.linha_importacao}
```{excecoes}

## Regras de negócio
{funcao.regras_md.strip()}

## O que se espera dos testes
- Cubra todas as regras (R1, R2, …).
- Inclua valores-limite (fronteiras) e entradas inválidas sempre que as regras os definirem.
- Cada expectativa (asserção) deve decorrer das regras. Não invente comportamento que as
  regras não definem e não teste o que está "fora do escopo".
- Indique qual regra cada caso verifica."""


def prompt_direta(funcao) -> str:
    return contexto_comum(funcao) + """

## Formato da resposta
Responda com UM arquivo pytest completo, dentro de um único bloco ```python ... ```.
- Use apenas pytest e a biblioteca padrão do Python.
- Importe a função exatamente como indicado acima.
- Coloque o identificador da regra no nome de cada teste (por exemplo, `test_r2_...`)."""


def prompt_plano(funcao) -> str:
    return contexto_comum(funcao) + """

## Formato da resposta
Responda APENAS com um objeto JSON (sem texto antes ou depois), no formato:

{"casos": [
  {"id": "C1", "regra": "R1", "tipo": "normal", "descricao": "o que o caso verifica",
   "entrada": {"args": [ ... ], "kwargs": { ... }},
   "esperado": {"retorno": <valor esperado>}},
  {"id": "C2", "regra": "R3", "tipo": "invalida", "descricao": "...",
   "entrada": {"args": [ ... ]},
   "esperado": {"excecao": "NomeDaExcecao"}}
]}

- "tipo" é "normal", "fronteira" ou "invalida".
- "args" e "kwargs" usam valores JSON (números, strings, true/false, null, listas).
- Para valores que JSON não representa, use {"$expr": "<expressão Python>"}, por exemplo
  {"$expr": "float('inf')"} ou {"$expr": "10**30"}. Só são permitidos literais, operações
  aritméticas e as funções float, int, str, bytes, list, tuple, set, dict, bool.
- Em "esperado", use "retorno" (valor que a função deve devolver) OU "excecao" (nome de uma
  exceção embutida do Python ou de uma das exceções listadas acima)."""


def prompt_reparo_plano(erros: list) -> str:
    lista = "\n".join(f"- {e}" for e in erros[:30])
    return f"""O plano tem problemas técnicos que impedem gerar os testes:
{lista}

Corrija SOMENTE esses problemas e devolva o JSON completo do plano, no mesmo formato,
sem texto fora do JSON."""


def prompt_reparo_coleta(erro: str) -> str:
    return f"""O arquivo de testes gerado a partir do plano não pôde ser carregado pelo pytest:

{erro[-1500:]}

Corrija o plano e devolva o JSON completo, no mesmo formato, sem texto fora do JSON."""
