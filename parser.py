import ply.yacc as yacc
from lexer import tokens
from ast_nodes import *

# ─── Precedence ───────────────────────────────────────────────────────────────
precedence = (
    ('left', 'OR'),
    ('left', 'AND'),
    ('right', 'NOT'),
    ('nonassoc', 'EQ', 'NEQ', 'LT', 'LE', 'GT', 'GE'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE', 'MOD'),
    ('right', 'UMINUS'),
)

# ─── Program ──────────────────────────────────────────────────────────────────
def p_program(p):
    '''program : stmt_list'''
    p[0] = Program(p[1])

def p_stmt_list(p):
    '''stmt_list : stmt_list stmt
                 | stmt'''
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = [p[1]]

# ─── Statements ───────────────────────────────────────────────────────────────
def p_stmt_fun_decl(p):
    '''stmt : FUN ID COLON type SEMI'''
    p[0] = FunDecl(p[2], p[4])

def p_stmt_let_value(p):
    '''stmt : LET ID COLON type ASSIGN expr SEMI'''
    p[0] = LetValue(p[2], p[4], p[6])

def p_stmt_let_fun(p):
    '''stmt : LET ID ID ASSIGN expr SEMI'''
    p[0] = LetFun(p[2], p[3], p[5])

def p_stmt_expr(p):
    '''stmt : expr SEMI'''
    p[0] = ExprStmt(p[1])

# ─── Types ────────────────────────────────────────────────────────────────────
def p_type_int(p):
    '''type : TINT'''
    p[0] = TypeInt()

def p_type_bool(p):
    '''type : TBOOL'''
    p[0] = TypeBool()

def p_type_fun(p):
    '''type : type ARROW type'''
    p[0] = TypeFun(p[1], p[3])

def p_type_paren(p):
    '''type : LPAREN type RPAREN'''
    p[0] = p[2]

# ─── Expressions ──────────────────────────────────────────────────────────────
def p_expr_binop(p):
    '''expr : expr PLUS expr
            | expr MINUS expr
            | expr TIMES expr
            | expr DIVIDE expr
            | expr MOD expr
            | expr EQ expr
            | expr NEQ expr
            | expr LT expr
            | expr LE expr
            | expr GT expr
            | expr GE expr
            | expr AND expr
            | expr OR expr'''
    p[0] = BinOp(p[2], p[1], p[3])

def p_expr_not(p):
    '''expr : NOT expr'''
    p[0] = UnaryOp('!', p[2])

def p_expr_uminus(p):
    '''expr : MINUS expr %prec UMINUS'''
    p[0] = UnaryOp('-', p[2])

def p_expr_if(p):
    '''expr : IF expr THEN expr ELSE expr'''
    p[0] = IfExpr(p[2], p[4], p[6])

def p_expr_when(p):
    '''expr : WHEN LPAREN expr RPAREN IS case_list END
            | WHEN expr IS case_list END'''
    if len(p) == 8:
        p[0] = WhenExpr(p[3], p[6])
    else:
        p[0] = WhenExpr(p[2], p[4])

def p_case_list(p):
    '''case_list : case_list case
                 | case'''
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = [p[1]]

def p_case(p):
    '''case : pat_list ARROW expr SEMI'''
    p[0] = (p[1], p[3])

def p_pat_list_multi(p):
    '''pat_list : pat_list COMMA pattern'''
    p[0] = p[1] + [p[3]]

def p_pat_list_single(p):
    '''pat_list : pattern'''
    p[0] = [p[1]]

def p_pattern_num(p):
    '''pattern : NUMBER'''
    p[0] = PatNum(p[1])

def p_pattern_neg(p):
    '''pattern : MINUS NUMBER'''
    p[0] = PatNeg(p[2])

def p_pattern_true(p):
    '''pattern : TRUE'''
    p[0] = PatBool(True)

def p_pattern_false(p):
    '''pattern : FALSE'''
    p[0] = PatBool(False)

def p_pattern_wild(p):
    '''pattern : UNDERSCORE'''
    p[0] = PatWild()

def p_expr_funcall(p):
    '''expr : ID LPAREN expr RPAREN'''
    p[0] = FunCall(p[1], p[3])

def p_expr_num(p):
    '''expr : NUMBER'''
    p[0] = Num(p[1])

def p_expr_true(p):
    '''expr : TRUE'''
    p[0] = Bool(True)

def p_expr_false(p):
    '''expr : FALSE'''
    p[0] = Bool(False)

def p_expr_var(p):
    '''expr : ID'''
    p[0] = Var(p[1])

def p_expr_paren(p):
    '''expr : LPAREN expr RPAREN'''
    p[0] = p[2]

def p_error(p):
    if p:
        raise SyntaxError(f"Syntax error at '{p.value}' (line {p.lineno})")
    else:
        raise SyntaxError("Syntax error at end of input")

parser = yacc.yacc(debug=False, write_tables=False)

def parse(data):
    return parser.parse(data)