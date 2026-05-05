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

### Expressões Aritméticas e Booleanas
Pode realizar cálculos e comparações básicas:
```lfun
10 + 5 * 2;         -- resultado: 20
(10 + 5) * 2;       -- resultado: 30
3 < 5;              -- resultado: true
10 == 10;           -- resultado: true
```

### Definição de Valores
Use `let` para definir constantes com tipo explícito:
```lfun
let x : Int = 42;
let ativo : Bool = true;
```

---

## 3. Funções e Recursividade

### Definindo Funções
As funções requerem uma assinatura de tipo (`fun`) seguida da definição (`let`):
```lfun
fun dobro : Int -> Int;
let dobro n = n * 2;

dobro(5);           -- resultado: 10
```

### Funções Recursivas
O LFun suporta recursividade. Certifique-se de que a assinatura de tipo está correta:
```lfun
fun fat : Int -> Int;
let fat n = if n == 0 then 1 else n * fat(n - 1);

fat(5);             -- resultado: 120
```

---

## 4. Novos Tipos: Char e String

### Char (Caracteres)
Representado por aspas simples:
```lfun
let letra : Char = 'A';
```

### String (Cadeias de Caracteres)
Representado por aspas duplas. Suporta concatenação com o operador `+`:
```lfun
let nome : String = "LFun";
let msg : String = "Ola, " + nome;
```

---

## 5. Seleção de Casos (Expression `when`)

O comando `when` permite fazer "pattern matching" em diversos tipos:

### Exemplo com Int
```lfun
fun eZero : Int -> Bool;
let eZero n =
  when (n) is
    0 -> true;
    _ -> false;
  end;
```

### Exemplo com Char e String
```lfun
fun nota : Char -> String;
let nota c =
  when c is
    'A' -> "Excelente";
    'B' -> "Bom";
    _   -> "Outra";
  end;
```

---

## 6. Dicas Úteis
- Todas as instruções de topo devem terminar com `;`.
- Comentários de linha começam com `--`.
- Comentários de bloco são delimitados por `{-` e `-}`.
- O intérprete realiza verificação semântica (tipagem) antes da execução.
