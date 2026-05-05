"""
Semantic analyser for LFun.
- Builds and maintains a symbol table
- Performs type checking
"""

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
    return t1 == t2


class TypeChecker:
    def __init__(self):
        self.symbols = SymbolTable()

    def check_program(self, program):
        # program is ('Program', stmts)
        for stmt in program[1]:
            self.check_stmt(stmt)

    def check_stmt(self, stmt):
        tag = stmt[0]
        if tag == 'FunDecl':
            # ('FunDecl', name, fun_type)
            self.symbols.define(stmt[1], stmt[2])

        elif tag == 'LetValue':
            # ('LetValue', name, val_type, expr)
            expr_type = self.infer(stmt[3])
            if not types_equal(expr_type, stmt[2]):
                raise SemanticError(
                    f"Type mismatch in 'let {stmt[1]}': declared {stmt[2]}, got {expr_type}"
                )
            self.symbols.define(stmt[1], stmt[2])

        elif tag == 'LetFun':
            # ('LetFun', name, param, expr)
            sig = self.symbols.lookup(stmt[1])
            if sig is None or sig[0] != 'TypeFun':
                raise SemanticError(
                    f"Function '{stmt[1]}' used in let without a prior 'fun' declaration"
                )
            # Type-check body with param in scope
            # Note: sig is ('TypeFun', param_type, return_type)
            self.symbols.push()
            self.symbols.define(stmt[2], sig[1])
            body_type = self.infer(stmt[3])
            self.symbols.pop()
            if not types_equal(body_type, sig[2]):
                raise SemanticError(
                    f"Function '{stmt[1]}' body type {body_type} does not match declared return type {sig[2]}"
                )

        elif tag == 'ExprStmt':
            # ('ExprStmt', expr)
            self.infer(stmt[1])

    def infer(self, expr):
        tag = expr[0]
        if tag == 'Num':
            return ('TypeInt',)

        if tag == 'Bool':
            return ('TypeBool',)
        
        if tag == 'Char':
            return ('TypeChar',)
        
        if tag == 'String':
            return ('TypeString',)

        if tag == 'Var':
            t = self.symbols.lookup(expr[1])
            if t is None:
                raise SemanticError(f"Undefined variable '{expr[1]}'")
            return t

        if tag == 'UnaryOp':
            op, subexpr = expr[1], expr[2]
            if op == '-':
                t = self.infer(subexpr)
                if t != ('TypeInt',):
                    raise SemanticError(f"Unary minus requires Int, got {t}")
                return ('TypeInt',)
            if op == '!':
                t = self.infer(subexpr)
                if t != ('TypeBool',):
                    raise SemanticError(f"Logical NOT requires Bool, got {t}")
                return ('TypeBool', )

        if tag == 'BinOp':
            op, left, right = expr[1], expr[2], expr[3]
            lt = self.infer(left)
            rt = self.infer(right)

            if op in ('+', '-', '*', '/', '%'):
                if op == '+' and lt == ('TypeString',) and rt == ('TypeString',):
                    return ('TypeString',)
                if lt != ('TypeInt',):
                    raise SemanticError(f"Operator '{op}' requires Int left operand, got {lt}")
                if rt != ('TypeInt',):
                    raise SemanticError(f"Operator '{op}' requires Int right operand, got {rt}")
                return ('TypeInt',)

            if op in ('<', '<=', '>', '>='):
                if lt != ('TypeInt',):
                    raise SemanticError(f"Operator '{op}' requires Int left operand, got {lt}")
                if rt != ('TypeInt',):
                    raise SemanticError(f"Operator '{op}' requires Int right operand, got {rt}")
                return ('TypeBool',)

            if op in ('==', '!='):
                if not types_equal(lt, rt):
                    raise SemanticError(
                        f"Operator '{op}' requires operands of same type, got {lt} and {rt}"
                    )
                return ('TypeBool',)

            if op in ('&&', '||'):
                if lt != ('TypeBool',):
                    raise SemanticError(f"Operator '{op}' requires Bool left operand, got {lt}")
                if rt != ('TypeBool',):
                    raise SemanticError(f"Operator '{op}' requires Bool right operand, got {rt}")
                return ('TypeBool',)

        if tag == 'If':
            # ('If', cond, then_expr, else_expr)
            ct = self.infer(expr[1])
            if ct != ('TypeBool',):
                raise SemanticError(f"'if' condition must be Bool, got {ct}")
            tt = self.infer(expr[2])
            et = self.infer(expr[3])
            if not types_equal(tt, et):
                raise SemanticError(
                    f"'if' branches have incompatible types: {tt} vs {et}"
                )
            return tt

        if tag == 'When':
            # ('When', expr, cases)
            scrutinee_type = self.infer(expr[1])
            result_type = None
            for patterns, result_expr in expr[2]:
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

        if tag == 'FunCall':
            # ('FunCall', name, arg)
            sig = self.symbols.lookup(expr[1])
            if sig is None:
                raise SemanticError(f"Undefined function '{expr[1]}'")
            if sig[0] != 'TypeFun':
                raise SemanticError(f"'{expr[1]}' is not a function")
            arg_type = self.infer(expr[2])
            if not types_equal(arg_type, sig[1]):
                raise SemanticError(
                    f"Function '{expr[1]}' expects {sig[1]}, got {arg_type}"
                )
            return sig[2]

        raise SemanticError(f"Unknown expression: {expr}")

    def _check_pattern(self, pat, scrutinee_type):
        tag = pat[0]
        if tag in ('PatNum', 'PatNeg'):
            if scrutinee_type != ('TypeInt',):
                raise SemanticError(f"Integer pattern used on non-Int scrutinee (type {scrutinee_type})")
        elif tag == 'PatBool':
            if scrutinee_type != ('TypeBool',):
                raise SemanticError(f"Boolean pattern used on non-Bool scrutinee (type {scrutinee_type})")
        elif tag == 'PatChar':
            if scrutinee_type != ('TypeChar',):
                raise SemanticError(f"Char pattern used on non-Char scrutinee (type {scrutinee_type})")
        elif tag == 'PatString':
            if scrutinee_type != ('TypeString',):
                raise SemanticError(f"String pattern used on non-String scrutinee (type {scrutinee_type})")
        # PatWild matches anything
