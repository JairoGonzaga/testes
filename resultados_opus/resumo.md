# Resultados

Modelo: arquivo/claude-opus-subagente. Funções: 5. Execuções: 10 (5 A, 5 B). Versão dos prompts: 56b903e055.

Cada função conta uma vez: primeiro tira-se a mediana das repetições de cada condição; depois, a diferença B − A por função. As colunas A e B mostram a mediana entre funções (para execuções utilizáveis, a proporção de todas as execuções). A coluna *B>A / = / B<A* conta funções.

## Comparação pareada (mediana entre funções)

| QP | Métrica | A (direta) | B (agente) | Mediana de B − A | B>A / = / B<A | Melhor quando |
|---|---|---|---|---|---|---|
| QP1 | Falsos alarmes | 0% | 0% | +0 p.p. | 0 / 5 / 0 | menor |
| QP2 | **Detecção de defeitos** | 100% | 100% | +0 p.p. | 0 / 5 / 0 | maior |
| QP2 | Mutation score | 100% | 100% | +0 p.p. | 0 / 3 / 2 | maior |
| QP3 | Cobertura de regras (automática) | 100% | 100% | +0 p.p. | 0 / 5 / 0 | maior |
| QP3 | Cobertura de fronteiras | 100% | 100% | +0 p.p. | 0 / 5 / 0 | maior |
| QP3 | Cobertura de ramos (auxiliar) | 100% | 100% | +0 p.p. | 0 / 5 / 0 | maior |
| QP4 | **Execuções utilizáveis** | 100% | 100% | +0 p.p. | 0 / 5 / 0 | maior |

Em negrito, a métrica principal de cada questão.

## Tamanho, custo e esforço (QP4) — mediana por execução

| Medida | A (direta) | B (agente) | Mediana de B − A |
|---|---|---|---|
| Testes gerados (casos) | 138 | 55 | -74 |
| Testes válidos | 138 | 55 | -74 |
| Chamadas | 1 | 1 | +0,0 |
| Tokens de entrada | 757 | 933 | +176 |
| Tokens de saída | 2.981 | 2.807 | +122 |
| Tempo (s) | 100 | 99,6 | +9,7 |

## Por função (mediana das repetições)

### QP1 — Falsos alarmes

| Função | A | B | B − A |
|---|---|---|---|
| cpf_validate | 0% | 0% | +0 p.p. |
| intword | 0% | 0% | +0 p.p. |
| luhn_validate | 0% | 0% | +0 p.p. |
| naturalsize | 0% | 0% | +0 p.p. |
| ordinal | 0% | 0% | +0 p.p. |

### QP2 — Detecção de defeitos

| Função | A | B | B − A |
|---|---|---|---|
| cpf_validate | 100% | 100% | +0 p.p. |
| intword | 100% | 100% | +0 p.p. |
| luhn_validate | 100% | 100% | +0 p.p. |
| naturalsize | 100% | 100% | +0 p.p. |
| ordinal | 100% | 100% | +0 p.p. |

### QP2 — Mutation score

| Função | A | B | B − A |
|---|---|---|---|
| cpf_validate | 100% | 97% | -3 p.p. |
| intword | 100% | 100% | +0 p.p. |
| luhn_validate | 100% | 100% | +0 p.p. |
| naturalsize | 100% | 100% | +0 p.p. |
| ordinal | 100% | 92% | -8 p.p. |

### QP3 — Cobertura de fronteiras

| Função | A | B | B − A |
|---|---|---|---|
| cpf_validate | 100% | 100% | +0 p.p. |
| intword | 100% | 100% | +0 p.p. |
| luhn_validate | 100% | 100% | +0 p.p. |
| naturalsize | 100% | 100% | +0 p.p. |
| ordinal | 100% | 100% | +0 p.p. |

### QP4 — Execuções utilizáveis

| Função | A | B | B − A |
|---|---|---|---|
| cpf_validate | 100% | 100% | +0 p.p. |
| intword | 100% | 100% | +0 p.p. |
| luhn_validate | 100% | 100% | +0 p.p. |
| naturalsize | 100% | 100% | +0 p.p. |
| ordinal | 100% | 100% | +0 p.p. |

## Limitações

- Com 5 funções a leitura é exploratória: não generaliza para outros modelos ou sistemas.
- A revisão não é totalmente cega: o estilo do código (template × livre) pode revelar a condição.
- Execuções não utilizáveis entram com 0 em detecção e cobertura (ver decisão no topo de analisar.py).
