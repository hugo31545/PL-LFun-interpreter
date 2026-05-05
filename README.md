# LFun — Interpretador da Linguagem Funcional

**Processamento de Linguagens — 2025/2026**

## Estrutura do Projeto

```
lfun/
├── lexer.py        # Analisador léxico (PLY lex)
├── parser.py       # Analisador sintático (PLY yacc)
├── semantic.py     # Análise semântica + verificação de tipos
├── interpreter.py  # Avaliador / interpretador da AST (Baseado em Tuplas)
├── main.py         # Ponto de entrada (REPL + ficheiros .lf)
├── entrada.lf      # Ficheiro de teste principal
├── TUTORIAL.md     # Guia de utilização e exemplos
└── teste_erro.lf   # Teste de deteção de erros semânticos
```

## Como Usar

### Executar um ficheiro `.lf`
```bash
python main.py entrada.lf
```

### Modo interativo (REPL)
```bash
python main.py
```

---

## Funcionalidades Implementadas

### A. Expressões
- **Aritméticas**: `+`, `-`, `*`, `/`, `%` com precedência correta
- **Booleanas**: `<`, `<=`, `>`, `>=`, `==`, `!=`, `&&`, `||`, `!`
- Parênteses para agrupar
- Unário negativo (`-expr`)

### B. Novos Tipos e Literais
- **Char**: Literais como `'a'`, `'B'`, etc.
- **String**: Literais como `"olá"`. Suporta concatenação com `+`.

### C. Definições e Funções
```lfun
let base : Int = 10;
let ativo : Bool = true;

fun inc : Int -> Int;
let inc x = x + 1;
inc(5);   -- resultado: 6  tipo: Int
```

### D. Recursividade
O interpretador suporta funções recursivas através de *recursive binding* no ambiente da closure:
```lfun
fun fat : Int -> Int;
let fat n = if n == 0 then 1 else n * fat(n - 1);
```

### E. Condicional e Seleção de Casos
- **if/then/else** para lógica condicional.
- **when ... is ... end** para pattern matching em `Int`, `Bool`, `Char` e `String`.

---

## Análise Semântica

O analisador semântico verifica:
- Tipos nas definições `let` correspondem à expressão.
- Tipos dos argumentos nas chamadas de funções.
- Suporte a recursividade (função declarada antes de ser definida).
- Compatibilidade de tipos em operações aritméticas, lógicas e de comparação.
- Concatenação de strings (`String + String`).

---

## Representação da AST (Tuplas)

A AST foi simplificada de classes para **tuplas**, tornando o processamento mais leve e a comparação de tipos mais direta:

| Tag          | Descrição                          |
|--------------|------------------------------------|
| `Num`        | Literal inteiro                    |
| `Bool`       | Literal booleano                   |
| `Char`       | Literal de caractere               |
| `String`     | Literal de cadeia de caracteres    |
| `Var`        | Referência a variável              |
| `BinOp`      | Operação binária                   |
| `UnaryOp`    | Operação unária (`-`, `!`)         |
| `If`         | Expressão condicional              |
| `When`       | Seleção de casos por padrões       |
| `FunCall`    | Chamada de função                  |
| `FunDecl`    | Declaração de assinatura de função |
| `LetValue`   | Definição de valor                 |
| `LetFun`     | Definição de função                |

---

## Dependências

- Python 3.8+
- PLY (`pip install ply`)
