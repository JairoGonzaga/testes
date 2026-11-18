# apnumber

Converte um inteiro para o estilo da Associated Press (AP): números de 0 a 9 são
escritos por extenso, em inglês.

## Regras

- **R1** — Para inteiros de 0 a 9 (inclusive), retorna o número por extenso, em inglês e
  em minúsculas: 0 → `"zero"`, 1 → `"one"`, 2 → `"two"`, 3 → `"three"`, 4 → `"four"`,
  5 → `"five"`, 6 → `"six"`, 7 → `"seven"`, 8 → `"eight"`, 9 → `"nine"`.
- **R2** — Para inteiros fora desse intervalo (negativos ou maiores que 9), retorna o
  número como string: 10 → `"10"`.
- **R3** — Antes de aplicar R1 e R2, o valor é convertido com `int()`. Assim, strings que
  contêm um inteiro (`"7"` → `"seven"`) e floats (que `int()` trunca) também são aceitos.
- **R4** — Se o valor não puder ser convertido com `int()`, a função retorna
  `str(value)`: `"foo"` → `"foo"`, `None` → `"None"`.
- **R5** — Valores não finitos: `float("inf")` → `"+Inf"`, `float("-inf")` → `"-Inf"`,
  `float("nan")` → `"NaN"`.

## Fora do escopo

- Valores booleanos (`True`, `False`).
