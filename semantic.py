"""
Semantic analyser for LFun.
- Builds and maintains a symbol table
- Performs type checking
"""

from ast_nodes import *


class SemanticError(Exception):
    pass


class SymbolTable:
    def __init__(self):
        self._scopes = [{}]

    def push(self):
        self._scopes.append({})

    def pop(self):
        self._scopes.pop()

    def define(self, name, typ):
        self._scopes[-1][name] = typ

    def lookup(self, name):
        for scope in reversed(self._scopes):
            if name in scope:
                return scope[name]
        return None


def types_equal(t1, t2):
    if type(t1) != type(t2):
        return False
    if isinstance(t1, TypeFun):
        return types_equal(t1.param_type, t2.param_type) and types_equal(t1.return_type, t2.return_type)
    return True


class TypeChecker:
    def __init__(self):
        self.symbols = SymbolTable()

    def check_program(self, program):
        for stmt in program.stmts:
            self.check_stmt(stmt)

    def check_stmt(self, stmt):
        if isinstance(stmt, FunDecl):
            self.symbols.define(stmt.name, stmt.fun_type)

        elif isinstance(stmt, LetValue):
            expr_type = self.infer(stmt.expr)
            if not types_equal(expr_type, stmt.val_type):
                raise SemanticError(
                    f"Type mismatch in 'let {stmt.name}': declared {stmt.val_type}, got {expr_type}"
                )
            self.symbols.define(stmt.name, stmt.val_type)

        elif isinstance(stmt, LetFun):
            # Look up previously declared signature
            sig = self.symbols.lookup(stmt.name)
            if sig is None or not isinstance(sig, TypeFun):
                raise SemanticError(
                    f"Function '{stmt.name}' used in let without a prior 'fun' declaration"
                )
            # Type-check body with param in scope
            self.symbols.push()
            self.symbols.define(stmt.param, sig.param_type)
            body_type = self.infer(stmt.expr)
            self.symbols.pop()
            if not types_equal(body_type, sig.return_type):
                raise SemanticError(
                    f"Function '{stmt.name}' body type {body_type} does not match declared return type {sig.return_type}"
                )

        elif isinstance(stmt, ExprStmt):
            self.infer(stmt.expr)

    def infer(self, expr):
        if isinstance(expr, Num):
            return TypeInt()

        if isinstance(expr, Bool):
            return TypeBool()

        if isinstance(expr, Var):
            t = self.symbols.lookup(expr.name)
            if t is None:
                raise SemanticError(f"Undefined variable '{expr.name}'")
            return t

        if isinstance(expr, UnaryOp):
            if expr.op == '-':
                t = self.infer(expr.expr)
                if not isinstance(t, TypeInt):
                    raise SemanticError(f"Unary minus requires Int, got {t}")
                return TypeInt()
            if expr.op == '!':
                t = self.infer(expr.expr)
                if not isinstance(t, TypeBool):
                    raise SemanticError(f"Logical NOT requires Bool, got {t}")
                return TypeBool()

        if isinstance(expr, BinOp):
            lt = self.infer(expr.left)
            rt = self.infer(expr.right)

            if expr.op in ('+', '-', '*', '/', '%'):
                if not isinstance(lt, TypeInt):
                    raise SemanticError(f"Operator '{expr.op}' requires Int left operand, got {lt}")
                if not isinstance(rt, TypeInt):
                    raise SemanticError(f"Operator '{expr.op}' requires Int right operand, got {rt}")
                return TypeInt()

            if expr.op in ('<', '<=', '>', '>='):
                if not isinstance(lt, TypeInt):
                    raise SemanticError(f"Operator '{expr.op}' requires Int left operand, got {lt}")
                if not isinstance(rt, TypeInt):
                    raise SemanticError(f"Operator '{expr.op}' requires Int right operand, got {rt}")
                return TypeBool()

            if expr.op in ('==', '!='):
                if not types_equal(lt, rt):
                    raise SemanticError(
                        f"Operator '{expr.op}' requires operands of same type, got {lt} and {rt}"
                    )
                return TypeBool()

            if expr.op in ('&&', '||'):
                if not isinstance(lt, TypeBool):
                    raise SemanticError(f"Operator '{expr.op}' requires Bool left operand, got {lt}")
                if not isinstance(rt, TypeBool):
                    raise SemanticError(f"Operator '{expr.op}' requires Bool right operand, got {rt}")
                return TypeBool()

        if isinstance(expr, IfExpr):
            ct = self.infer(expr.cond)
            if not isinstance(ct, TypeBool):
                raise SemanticError(f"'if' condition must be Bool, got {ct}")
            tt = self.infer(expr.then_expr)
            et = self.infer(expr.else_expr)
            if not types_equal(tt, et):
                raise SemanticError(
                    f"'if' branches have incompatible types: {tt} vs {et}"
                )
            return tt

        if isinstance(expr, WhenExpr):
            scrutinee_type = self.infer(expr.expr)
            result_type = None
            for patterns, result_expr in expr.cases:
                # Check patterns are compatible with scrutinee
                for pat in patterns:
                    self._check_pattern(pat, scrutinee_type)
                rt = self.infer(result_expr)
                if result_type is None:
                    result_type = rt
                elif not types_equal(result_type, rt):
                    raise SemanticError(
                        f"'when' cases have incompatible types: {result_type} vs {rt}"
                    )
            return result_type

        if isinstance(expr, FunCall):
            sig = self.symbols.lookup(expr.name)
            if sig is None:
                raise SemanticError(f"Undefined function '{expr.name}'")
            if not isinstance(sig, TypeFun):
                raise SemanticError(f"'{expr.name}' is not a function")
            arg_type = self.infer(expr.arg)
            if not types_equal(arg_type, sig.param_type):
                raise SemanticError(
                    f"Function '{expr.name}' expects {sig.param_type}, got {arg_type}"
                )
            return sig.return_type

        raise SemanticError(f"Unknown expression: {expr}")

    def _check_pattern(self, pat, scrutinee_type):
        if isinstance(pat, (PatNum, PatNeg)):
            if not isinstance(scrutinee_type, TypeInt):
                raise SemanticError(
                    f"Integer pattern used on non-Int scrutinee (type {scrutinee_type})"
                )
        elif isinstance(pat, PatBool):
            if not isinstance(scrutinee_type, TypeBool):
                raise SemanticError(
                    f"Boolean pattern used on non-Bool scrutinee (type {scrutinee_type})"
                )
        # PatWild matches anything