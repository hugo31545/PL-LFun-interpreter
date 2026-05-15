"""
Interpreter for LFun language.
Walks the AST and evaluates expressions.
"""

from ast_nodes import *


class RuntimeError_(Exception):
    pass


class Environment:
    def __init__(self, parent=None):
        self._bindings = {}
        self._parent = parent

    def define(self, name, value):
        self._bindings[name] = value

    def lookup(self, name):
        if name in self._bindings:
            return self._bindings[name]
        if self._parent:
            return self._parent.lookup(name)
        raise RuntimeError_(f"Undefined variable '{name}'")


class Closure:
    """Represents a function value."""
    def __init__(self, param, body, env):
        self.param = param
        self.body = body
        self.env = env

    def __repr__(self):
        return f"<function>"


class Interpreter:
    def __init__(self):
        self.env = Environment()

    def run_program(self, program):
        results = []
        for stmt in program.stmts:
            r = self.run_stmt(stmt)
            if r is not None:
                results.append(r)
        return results

    def run_stmt(self, stmt):
        if isinstance(stmt, FunDecl):
            # Just a type signature, no runtime action needed
            return None

        if isinstance(stmt, LetValue):
            val = self.eval(stmt.expr, self.env)
            self.env.define(stmt.name, val)
            return None

        if isinstance(stmt, LetFun):
            closure = Closure(stmt.param, stmt.expr, self.env)
            self.env.define(stmt.name, closure)
            return None

        if isinstance(stmt, ExprStmt):
            return self.eval(stmt.expr, self.env)

    def eval(self, expr, env):
        if isinstance(expr, Num):
            return expr.value

        if isinstance(expr, Bool):
            return expr.value

        if isinstance(expr, Var):
            return env.lookup(expr.name)

        if isinstance(expr, UnaryOp):
            v = self.eval(expr.expr, env)
            if expr.op == '-':
                return -v
            if expr.op == '!':
                return not v

        if isinstance(expr, BinOp):
            l = self.eval(expr.left, env)
            r = self.eval(expr.right, env)
            ops = {
                '+': lambda a, b: a + b,
                '-': lambda a, b: a - b,
                '*': lambda a, b: a * b,
                '/': lambda a, b: a // b,
                '%': lambda a, b: a % b,
                '<': lambda a, b: a < b,
                '<=': lambda a, b: a <= b,
                '>': lambda a, b: a > b,
                '>=': lambda a, b: a >= b,
                '==': lambda a, b: a == b,
                '!=': lambda a, b: a != b,
                '&&': lambda a, b: a and b,
                '||': lambda a, b: a or b,
            }
            return ops[expr.op](l, r)

        if isinstance(expr, IfExpr):
            cond = self.eval(expr.cond, env)
            if cond:
                return self.eval(expr.then_expr, env)
            else:
                return self.eval(expr.else_expr, env)

        if isinstance(expr, WhenExpr):
            val = self.eval(expr.expr, env)
            for patterns, result_expr in expr.cases:
                for pat in patterns:
                    if self._match(pat, val):
                        return self.eval(result_expr, env)
            raise RuntimeError_(f"Non-exhaustive patterns in 'when' expression (value: {val})")

        if isinstance(expr, FunCall):
            closure = env.lookup(expr.name)
            if not isinstance(closure, Closure):
                raise RuntimeError_(f"'{expr.name}' is not a function")
            arg_val = self.eval(expr.arg, env)
            new_env = Environment(closure.env)
            new_env.define(closure.param, arg_val)
            return self.eval(closure.body, new_env)

        raise RuntimeError_(f"Unknown expression node: {expr}")

    def _match(self, pattern, value):
        if isinstance(pattern, PatNum):
            return value == pattern.value
        if isinstance(pattern, PatNeg):
            return value == -pattern.value
        if isinstance(pattern, PatBool):
            return value == pattern.value
        if isinstance(pattern, PatWild):
            return True
        return False


def format_value(val, typ=None):
    """Format a value for display."""
    if isinstance(val, bool):
        return 'true' if val else 'false'
    return str(val)