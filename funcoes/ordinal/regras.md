# ordinal

Converte um inteiro para a sua forma ordinal em inglês (1st, 2nd, 3rd…).

## Regras

- **R1** — Retorna o inteiro seguido do sufixo ordinal, escolhido pelo último dígito:
  1 → `"st"`, 2 → `"nd"`, 3 → `"rd"`; 0 e 4 a 9 → `"th"`.
  Exemplos: 1 → `"1st"`, 1002 → `"1002nd"`, 103 → `"103rd"`, 4 → `"4th"`.
- **R2** — Exceção a R1: quando os dois últimos dígitos são 11, 12 ou 13, o sufixo é
  sempre `"th"`. Exemplos: 12 → `"12th"`, 111 → `"111th"`.
- **R3** — O valor é convertido com `int()` antes de aplicar R1 e R2. Strings que
  contêm um inteiro (`"5"` → `"5th"`) e floats (que `int()` trunca) também são aceitos.
- **R4** — Se o valor não puder ser convertido com `int()`, a função retorna
  `str(value)`: `"something else"` → `"something else"`, `[1, 2, 3]` → `"[1, 2, 3]"`.
- **R5** — O parâmetro `gender` aceita `"male"` (padrão) ou `"female"`. Em inglês o
  resultado é o mesmo para os dois valores.
- **R6** — Valores não finitos: `float("inf")` → `"+Inf"`, `float("-inf")` → `"-Inf"`,
  `float("nan")` → `"NaN"`.

## Fora do escopo

- Números negativos.
- Valores de `gender` diferentes de `"male"` e `"female"`.
