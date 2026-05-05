# Tutorial: Como usar o Intérprete LFun

Bem-vindo ao tutorial da linguagem **LFun** (Linguagem Funcional). Este guia explica como executar o intérprete e utilizar as suas principais funcionalidades (versão básica).

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

### Expressões Aritméticas e Booleanas
Pode realizar cálculos e comparações básicas entre inteiros e booleanos:
```lfun
10 + 5 * 2;         -- resultado: 20
(10 + 5) * 2;       -- resultado: 30
3 < 5;              -- resultado: true
10 == 10;           -- resultado: true
```

### Definição de Valores
Use `let` para definir constantes com tipo explícito (`Int` ou `Bool`):
```lfun
let x : Int = 42;
let ativo : Bool = true;
```

---

## 3. Funções

### Definindo Funções
As funções requerem uma assinatura de tipo (`fun`) seguida da definição (`let`):
```lfun
fun inc : Int -> Int;
let inc x = x + 1;

inc(5);           -- resultado: 6
```

Note que nesta versão o suporte a recursividade direta e tipos complexos como Strings/Chars não está ativo.

---

## 4. Seleção de Casos (Expression `when`)

O comando `when` permite fazer "pattern matching" em valores `Int` e `Bool`:

### Exemplo com Int
```lfun
fun eZero : Int -> Bool;
let eZero n =
  when (n) is
    0 -> true;
    _ -> false;
  end;
```

### Exemplo com Bool
```lfun
fun inverter : Bool -> Bool;
let inverter b =
  when b is
    true  -> false;
    false -> true;
  end;
```

---

## 5. Dicas Úteis
- Todas as instruções de topo devem terminar com `;`.
- Comentários de linha começam com `--`.
- Comentários de bloco são delimitados por `{-` e `-}`.
- O intérprete realiza verificação semântica antes da execução.
