# validate (Luhn)

Verifica se um número passa no algoritmo de Luhn (usado, por exemplo, em números de
cartão de crédito).

Exceções (todas podem ser importadas de `alvo`):

- `ValidationError` — base de todas, subclasse de `ValueError`;
- `InvalidFormat` — subclasse de `ValidationError`;
- `InvalidChecksum` — subclasse de `ValidationError`.

## Regras

- **R1** — Se `number` for "falso" em Python (string vazia, `None`, `0`), levanta
  `InvalidFormat`.
- **R2** — Todo caractere de `str(number)` precisa estar em `alphabet` (padrão
  `"0123456789"`); caso contrário, levanta `InvalidFormat`. Não há limpeza de
  separadores: `"7992 7398 713"` → `InvalidFormat`.
- **R3** — Soma de Luhn, com `n = len(alphabet)` e o valor de cada caractere igual à sua
  posição em `alphabet`: percorrendo da direita para a esquerda, os caracteres em
  posições ímpares (1ª, 3ª, …) somam o próprio valor; os em posições pares (2ª, 4ª, …)
  têm o valor dobrado e somam `(2·v) // n + (2·v) % n`. O número é válido quando a soma
  total é múltipla de `n`.
- **R4** — Se a soma não for múltipla de `n`, levanta `InvalidChecksum`:
  `"79927398710"` → `InvalidChecksum`.
- **R5** — Se o número for válido, retorna o próprio `number`, sem alteração e com o mesmo
  tipo recebido: `"79927398713"` → `"79927398713"`.
- **R6** — `alphabet` permite usar outras bases. Por exemplo, com
  `alphabet="0123456789abcdef"` (n = 16), `"1a2b1"` é válido. As letras diferenciam
  maiúsculas de minúsculas.

## Fora do escopo

- Alfabetos com caracteres repetidos.
