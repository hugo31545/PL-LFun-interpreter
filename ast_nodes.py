"""
Abstract Syntax Tree node definitions for LFun language.
"""

class ASTNode:
    pass

# --- Types ---
class TypeInt(ASTNode):
    def __repr__(self): return "Int"

class TypeBool(ASTNode):
    def __repr__(self): return "Bool"

class TypeFun(ASTNode):
    def __init__(self, param_type, return_type):
        self.param_type = param_type
        self.return_type = return_type
    def __repr__(self): return f"{self.param_type} -> {self.return_type}"

# --- Expressions ---
class Num(ASTNode):
    def __init__(self, value):
        self.value = value
    def __repr__(self): return f"Num({self.value})"

class Bool(ASTNode):
    def __init__(self, value):
        self.value = value
    def __repr__(self): return f"Bool({self.value})"

class Var(ASTNode):
    def __init__(self, name):
        self.name = name
    def __repr__(self): return f"Var({self.name})"

class BinOp(ASTNode):
    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right
    def __repr__(self): return f"BinOp({self.op}, {self.left}, {self.right})"

class UnaryOp(ASTNode):
    def __init__(self, op, expr):
        self.op = op
        self.expr = expr
    def __repr__(self): return f"UnaryOp({self.op}, {self.expr})"

class IfExpr(ASTNode):
    def __init__(self, cond, then_expr, else_expr):
        self.cond = cond
        self.then_expr = then_expr
        self.else_expr = else_expr
    def __repr__(self): return f"If({self.cond}, {self.then_expr}, {self.else_expr})"

class WhenExpr(ASTNode):
    """when (expr) is pat1, pat2 -> result1 ; pat3 -> result2 ; ... end"""
    def __init__(self, expr, cases):
        self.expr = expr
        self.cases = cases  # list of (patterns, result_expr)
    def __repr__(self): return f"When({self.expr}, {self.cases})"

class FunCall(ASTNode):
    def __init__(self, name, arg):
        self.name = name
        self.arg = arg
    def __repr__(self): return f"FunCall({self.name}, {self.arg})"

# --- Patterns ---
class PatNum(ASTNode):
    def __init__(self, value):
        self.value = value
    def __repr__(self): return f"PatNum({self.value})"

class PatNeg(ASTNode):
    def __init__(self, value):
        self.value = value
    def __repr__(self): return f"PatNeg({self.value})"

class PatBool(ASTNode):
    def __init__(self, value):
        self.value = value
    def __repr__(self): return f"PatBool({self.value})"

class PatWild(ASTNode):
    def __repr__(self): return "PatWild"

# --- Top-level declarations ---
class FunDecl(ASTNode):
    """fun name : type;"""
    def __init__(self, name, fun_type):
        self.name = name
        self.fun_type = fun_type
    def __repr__(self): return f"FunDecl({self.name}, {self.fun_type})"

class LetValue(ASTNode):
    """let name : type = expr;"""
    def __init__(self, name, val_type, expr):
        self.name = name
        self.val_type = val_type
        self.expr = expr
    def __repr__(self): return f"LetValue({self.name}, {self.val_type}, {self.expr})"

class LetFun(ASTNode):
    """let name param = expr;"""
    def __init__(self, name, param, expr):
        self.name = name
        self.param = param
        self.expr = expr
    def __repr__(self): return f"LetFun({self.name}, {self.param}, {self.expr})"

class ExprStmt(ASTNode):
    """expr;  — top-level expression to evaluate"""
    def __init__(self, expr):
        self.expr = expr
    def __repr__(self): return f"ExprStmt({self.expr})"

class Program(ASTNode):
    def __init__(self, stmts):
        self.stmts = stmts
    def __repr__(self): return f"Program({self.stmts})"
