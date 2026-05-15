import ply.lex as lex

# Reserved words
reserved = {
    'let'   : 'LET',
    'fun'   : 'FUN',
    'if'    : 'IF',
    'then'  : 'THEN',
    'else'  : 'ELSE',
    'when'  : 'WHEN',
    'is'    : 'IS',
    'end'   : 'END',
    'true'  : 'TRUE',
    'false' : 'FALSE',
    'Int'   : 'TINT',
    'Bool'  : 'TBOOL',
}

tokens = [
    'ID',
    'NUMBER',
    'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'MOD',
    'EQ', 'NEQ', 'LT', 'LE', 'GT', 'GE',
    'AND', 'OR', 'NOT',
    'ASSIGN',
    'ARROW',
    'COLON', 'SEMI', 'COMMA',
    'LPAREN', 'RPAREN',
    'UNDERSCORE',
] + list(reserved.values())

# Simple tokens
t_PLUS      = r'\+'
t_MINUS     = r'-'
t_TIMES     = r'\*'
t_DIVIDE    = r'/'
t_MOD       = r'%'
t_EQ        = r'=='
t_NEQ       = r'!='
t_LE        = r'<='
t_GE        = r'>='
t_LT        = r'<'
t_GT        = r'>'
t_AND       = r'&&'
t_OR        = r'\|\|'
t_NOT       = r'!'
t_ASSIGN    = r'='
t_ARROW     = r'->'
t_COLON     = r':'
t_SEMI      = r';'
t_COMMA     = r','
t_LPAREN    = r'\('
t_RPAREN    = r'\)'
t_UNDERSCORE = r'_'

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_ID(t):
    r'[a-zA-Z][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, 'ID')
    return t

# Single-line comments
def t_COMMENT_LINE(t):
    r'--[^\n]*'
    pass

# Multi-line comments {- ... -}
def t_COMMENT_BLOCK(t):
    r'\{-(.|\n)*?-\}'
    t.lexer.lineno += t.value.count('\n')

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

t_ignore = ' \t\r'

def t_error(t):
    print(f"Illegal character '{t.value[0]}' at line {t.lineno}")
    t.lexer.skip(1)

lexer = lex.lex()

def tokenize(data):
    lexer.input(data)
    return list(lexer)