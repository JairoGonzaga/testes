# Rodada rápida com Claude Opus (subagentes)

Rodada de demonstração feita em 17/11/2026, antes da coleta oficial. **Não substitui a
coleta da metodologia**: tem uma só repetição e não passou pela revisão manual.

## Como foi feita

- 5 funções × 2 condições × 1 repetição = 10 execuções, com o provedor `arquivo`.
- Cada prompt gerado pelo `gerar.py` foi entregue a um **subagente Claude Opus novo**,
  que só leu o arquivo do prompt. Ele não viu o código de referência, o gabarito nem os
  defeitos, e as respostas foram gravadas sem edição em `respostas_opus/`.
- Depois rodaram `executar.py --entrada execucoes_opus` e `analisar.py --entrada execucoes_opus`.

## Resultado

| Métrica | A (direta) | B (agente) |
|---|---|---|
| Execuções utilizáveis | 5/5 | 5/5 |
| Falsos alarmes (testes que falham na versão correta) | 0% | 0% |
| Detecção de defeitos | 100% nas 5 funções | 100% nas 5 funções |
| Mutation score | 100% nas 5 funções | 100% em 3; 97% no CPF; 92% no ordinal |
| Cobertura de fronteiras | 100% | 100% |
| Testes gerados (mediana) | 138 | 55 |
| Chamadas ao modelo | 1 | 1 (nenhum plano precisou de reparo) |

## Leitura

- **Efeito teto:** com um modelo forte como o Opus, as duas condições acertaram quase tudo.
  As funções e os defeitos não foram difíceis o bastante para separar os métodos.
- A única diferença apareceu no mutation score. O plano do agente para `ordinal` não teve
  números terminados em 6 e 8, e o do CPF não teve um caso com a letra "X". Com isso,
  3 mutantes sobreviveram. A geração direta produziu ~2,5× mais casos e matou todos.
- Nenhuma das duas caiu na "armadilha" do CPF com dígitos repetidos (R7): as duas trataram
  `111.111.111-11` como válido, como diz a regra.
- O agente não precisou de reparo: os 5 planos já vieram válidos na primeira chamada.

## Limitações desta rodada

- Uma repetição só: não dá para ver a variação entre execuções.
- Subagente não é uma chamada de API pura: há um prompt de sistema do agente por baixo.
- Tokens aproximados (caracteres ÷ 4). O tempo inclui a sobrecarga do subagente.
- Sem revisão manual: "expectativas corretas" e "cobertura de regras pela revisão" ficaram
  em branco. Os 0% de falsos alarmes indicam que nenhuma expectativa contradiz a versão correta.

## O que isso sugere para a coleta oficial

Para que a comparação mostre diferença, vale usar na coleta um modelo menor e mais barato
(onde erros de oráculo e de cobertura são mais prováveis) e/ou incluir funções com regras
mais difíceis. As duas escolhas precisam ser registradas no relatório.
