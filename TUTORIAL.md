# Tutorial: Como usar o Intérprete LFun

Bem-vindo ao tutorial da linguagem **LFun** (Linguagem Funcional). Este guia explica como executar o intérprete e utilizar as suas principais funcionalidades.

## 1. Como Executar

O intérprete suporta dois modos de funcionamento:

### Modo Interativo (REPL)
Para entrar no modo interativo, execute:
```bash
python main.py
```
No REPL, pode digitar expressões e definições linha a linha. Termine cada instrução com `;`. Uma linha em branco ou o comando `exit` sai do programa.

### Modo de Ficheiro
Para executar um script guardado num ficheiro `.lf`:
```bash
python main.py seu_ficheiro.lf
```

---

## 2. Sintaxe Básica

### A. Expressões Aritméticas e Booleanas
Pode realizar cálculos e comparações básicas entre inteiros e booleanos:
```lfun
3 + 4;          -- resultado: 7   tipo: Int
10 - 2 * 3;     -- resultado: 4   tipo: Int
(8 + 2) * 5;    -- resultado: 50  tipo: Int
3 < 5;          -- resultado: true  tipo: Bool
10 == 7;        -- resultado: false tipo: Bool
```

Os operadores lógicos também estão disponíveis:
```lfun
(true || false) && (!false);  -- resultado: true  tipo: Bool
```

### B. Definição de Valores
Use `let` para definir constantes com tipo explícito (`Int` ou `Bool`):
```lfun
let x : Int = 42;
let ativo : Bool = true;
let area : Int = largura * altura;
```

O analisador semântico rejeita declarações com tipo errado:
```lfun
let valor : Int = true;  -- Erro: Type mismatch
```

---

## 3. Funções (C)

As funções requerem uma assinatura de tipo (`fun`) seguida da definição (`let`):
```lfun
fun inc : Int -> Int;
let inc x = x + 1;

inc(5);   -- resultado: 6  tipo: Int
```

```lfun
fun ePositivo : Int -> Bool;
let ePositivo n = n > 0;

ePositivo(3);   -- resultado: true
ePositivo(-2);  -- resultado: false
```

---

## 4. Condicional e Seleção de Casos (D)

### if / then / else
```lfun
fun absoluto : Int -> Int;
let absoluto n = if n < 0 then 0 - n else n;

absoluto(-5);  -- resultado: 5  tipo: Int
absoluto(8);   -- resultado: 8  tipo: Int
```

### when / is / end (pattern matching)
O `when` permite associar padrões a resultados diferentes.  
Cada caso é separado por `;` e pode ter múltiplos padrões (`pat1, pat2 ->`):

```lfun
fun eZero : Int -> Bool;
let eZero n =
  when (n) is
    0 -> true;
    _ -> false;
  end;

eZero(0);  -- resultado: true
eZero(3);  -- resultado: false
```

```lfun
fun avalia : Int -> Bool;
let avalia x =
  when (x) is
    -1, 1 -> true;   -- múltiplos padrões alternativos
    0     -> false;
    _     -> true;   -- wildcard (otherwise)
  end;
```

```lfun
fun boolToInt : Bool -> Int;
let boolToInt b =
  when b is
    true  -> 1;
    false -> 0;
  end;
```

---

## 5. Comentários (E)

- **Linha única:** tudo após `--` é ignorado até ao fim da linha.
- **Multi-linha:** delimitados por `{-` e `-}`.

```lfun
-- isto é um comentário de linha

{-
  isto é um
  comentário de bloco
-}
```

---

## 6. Dicas úteis
- Todas as instruções de topo devem terminar com `;`.
- O intérprete realiza verificação semântica antes da execução.
- A precedência dos operadores segue as convenções matemáticas habituais: `*`, `/`, `%` têm prioridade sobre `+`, `-`; os operadores relacionais têm prioridade sobre os lógicos.
