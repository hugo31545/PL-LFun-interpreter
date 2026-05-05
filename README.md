# LFun — Interpretador da Linguagem Funcional

**Processamento de Linguagens — 2025/2026**

## Estrutura do Projeto

```
lfun/
├── lexer.py        # Analisador léxico (PLY lex)
├── parser.py       # Analisador sintático (PLY yacc)
├── ast_nodes.py    # Nós da Árvore de Sintaxe Abstrata (AST)
├── semantic.py     # Análise semântica + verificação de tipos
├── interpreter.py  # Avaliador / interpretador da AST
├── main.py         # Ponto de entrada (REPL + ficheiros .lf)
├── entrada.lf      # Ficheiro de teste principal
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

## Funcionalidades Implementadas

### A. Expressões
- **Aritméticas**: `+`, `-`, `*`, `/`, `%` com precedência correta
- **Booleanas**: `<`, `<=`, `>`, `>=`, `==`, `!=`, `&&`, `||`, `!`
- Parênteses para agrupar
- Unário negativo (`-expr`)

### B. Definições
```
let base : Int = 10;
let ativo : Bool = true;
let area : Int = largura * altura;
```

### C. Funções
```
fun inc : Int -> Int;
let inc x = x + 1;
inc(5);   -- resultado: 6  tipo: Int
```

### D. Condicional e seleção de casos
```
-- if/then/else
let absoluto n = if n < 0 then 0 - n else n;

-- when ... is ... end
let eZero n =
  when (n) is
    0 -> true;
    _ -> false;
  end;
```

### E. Comentários
- Linha única: `-- comentário`
- Multi-linha: `{- comentário -}`

## Análise Semântica

O analisador semântico verifica:
- Tipos nas definições `let` correspondem à expressão
- Tipos dos argumentos nas chamadas de funções
- Tipos dos dois ramos do `if` são compatíveis
- Todos os casos do `when` produzem o mesmo tipo
- Operadores aritméticos só aceitam `Int`
- Operadores de comparação `<`, `<=`, `>`, `>=` só aceitam `Int`
- Operadores lógicos `&&`, `||`, `!` só aceitam `Bool`

### Exemplo de erro detetado
```
let valor : Int = true;
-- Error: Type mismatch in 'let valor': declared Int, got Bool
```

## AST — Nós Principais

| Nó         | Descrição                          |
|------------|------------------------------------|
| `Num`      | Literal inteiro                    |
| `Bool`     | Literal booleano                   |
| `Var`      | Referência a variável              |
| `BinOp`    | Operação binária                   |
| `UnaryOp`  | Operação unária (`-`, `!`)         |
| `IfExpr`   | Expressão condicional              |
| `WhenExpr` | Seleção de casos por padrões       |
| `FunCall`  | Chamada de função                  |
| `FunDecl`  | Declaração de assinatura de função |
| `LetValue` | Definição de valor                 |
| `LetFun`   | Definição de função                |

## Dependências

- Python 3.8+
- PLY (`pip install ply`)
# PL-LFun-interpreter
