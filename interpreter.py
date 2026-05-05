"""
Interpreter for LFun language.
Walks the AST (tuple-based) and evaluates expressions.
"""

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
        # program is ('Program', stmts)
        results = []
        for stmt in program[1]:
            r = self.run_stmt(stmt)
            if r is not None:
                results.append(r)
        return results

    def run_stmt(self, stmt):
        tag = stmt[0]
        if tag == 'FunDecl':
            # Just a type signature, no runtime action needed
            return None

        if tag == 'LetValue':
            # ('LetValue', name, type, expr)
            val = self.eval(stmt[3], self.env)
            self.env.define(stmt[1], val)
            return None

        if tag == 'LetFun':
            # ('LetFun', name, param, expr)
            name, param, body = stmt[1], stmt[2], stmt[3]
            # To support recursion, the closure's environment must contain the function itself.
            # We create a new environment scope for the closure.
            closure_env = Environment(self.env)
            closure = Closure(param, body, closure_env)
            closure_env.define(name, closure) # Recursive binding
            self.env.define(name, closure)
            return None

        if tag == 'ExprStmt':
            # ('ExprStmt', expr)
            return self.eval(stmt[1], self.env)

    def eval(self, expr, env):
        tag = expr[0]
        
        if tag == 'Num':
            return expr[1]

        if tag == 'Bool':
            return expr[1]
        
        if tag == 'Char':
            return expr[1]
        
        if tag == 'String':
            return expr[1]

        if tag == 'Var':
            return env.lookup(expr[1])

        if tag == 'UnaryOp':
            op, subexpr = expr[1], expr[2]
            v = self.eval(subexpr, env)
            if op == '-':
                return -v
            if op == '!':
                return not v

        if tag == 'BinOp':
            op, left_expr, right_expr = expr[1], expr[2], expr[3]
            l = self.eval(left_expr, env)
            r = self.eval(right_expr, env)
            
            # String concatenation support (common extra)
            if op == '+' and isinstance(l, str) and isinstance(r, str):
                return l + r
                
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
            return ops[op](l, r)

        if tag == 'If':
            # ('If', cond, then_expr, else_expr)
            cond = self.eval(expr[1], env)
            if cond:
                return self.eval(expr[2], env)
            else:
                return self.eval(expr[3], env)

        if tag == 'When':
            # ('When', expr, cases)
            val = self.eval(expr[1], env)
            for patterns, result_expr in expr[2]:
                for pat in patterns:
                    if self._match(pat, val):
                        return self.eval(result_expr, env)
            raise RuntimeError_(f"Non-exhaustive patterns in 'when' expression (value: {val})")

        if tag == 'FunCall':
            # ('FunCall', name, arg)
            name, arg_expr = expr[1], expr[2]
            closure = env.lookup(name)
            if not isinstance(closure, Closure):
                raise RuntimeError_(f"'{name}' is not a function")
            arg_val = self.eval(arg_expr, env)
            new_env = Environment(closure.env)
            new_env.define(closure.param, arg_val)
            return self.eval(closure.body, new_env)

        raise RuntimeError_(f"Unknown expression tag: {tag}")

    def _match(self, pattern, value):
        tag = pattern[0]
        if tag == 'PatNum':
            return value == pattern[1]
        if tag == 'PatNeg':
            return value == -pattern[1]
        if tag == 'PatBool':
            return value == pattern[1]
        if tag == 'PatChar':
            return value == pattern[1]
        if tag == 'PatString':
            return value == pattern[1]
        if tag == 'PatWild':
            return True
        return False


def format_value(val):
    """Format a value for display."""
    if isinstance(val, bool):
        return 'true' if val else 'false'
    if isinstance(val, str) and len(val) == 1:
        return f"'{val}'"
    if isinstance(val, str):
        return f'"{val}"'
    return str(val)
