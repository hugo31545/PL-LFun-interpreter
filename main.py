#!/usr/bin/env python3
"""
LFun Interpreter — main entry point.

Usage:
    python main.py                   # Interactive REPL
    python main.py entrada.lf        # Run a .lf file
"""

import sys
import os

from lexer import lexer
from parser import parse
from semantic import TypeChecker, SemanticError
from interpreter import Interpreter, format_value


def type_str(t):
    tag = t[0]
    if tag == 'TypeInt':  return "Int"
    if tag == 'TypeBool': return "Bool"
    if tag == 'TypeChar': return "Char"
    if tag == 'TypeString': return "String"
    if tag == 'TypeFun':  return f"{type_str(t[1])} -> {type_str(t[2])}"
    return "?"


def run_source(source, checker, interp):
    """Parse, type-check and evaluate a source string. Returns list of result lines."""
    ast = parse(source)
    checker.check_program(ast)

    output = []
    # ast is ('Program', stmts)
    for stmt in ast[1]:
        if stmt[0] == 'ExprStmt':
            # Determine type before evaluating
            try:
                typ = checker.infer(stmt[1])
            except Exception:
                typ = None

            val = interp.run_stmt(stmt)
            t_label = type_str(typ) if typ else "?"
            output.append(f"resultado: {format_value(val)}  tipo: {t_label}")
        else:
            interp.run_stmt(stmt)
    return output


def run_file(path):
    checker = TypeChecker()
    interp  = Interpreter()

    try:
        with open(path, 'r', encoding='utf-8') as f:
            source = f.read()
    except FileNotFoundError:
        print(f"Error: file '{path}' not found.")
        sys.exit(1)

    try:
        lines = run_source(source, checker, interp)
        for line in lines:
            print(line)
    except (SyntaxError, SemanticError) as e:
        print(f"Error: {e}")
        sys.exit(1)


def repl():
    print("LFun Interpreter  (Ctrl+D or 'exit' to quit)")
    print("Multi-line: end each statement with ';'  |  Blank line to evaluate buffer\n")

    checker = TypeChecker()
    interp  = Interpreter()
    buf = []

    while True:
        prompt = "lfun> " if not buf else "    | "
        try:
            line = input(prompt)
        except EOFError:
            print()
            break

        if line.strip() == 'exit':
            break

        buf.append(line)

        # Try to evaluate when buffer seems complete (all ';' balanced, no open blocks)
        combined = '\n'.join(buf)
        # Simple heuristic: attempt parse on every non-empty line ending with ';' or on blank line
        if line.strip() == '' or line.strip().endswith(';') or line.strip() == 'end;':
            if combined.strip():
                try:
                    results = run_source(combined, checker, interp)
                    for r in results:
                        print(r)
                except SyntaxError as e:
                    # Might be incomplete input — keep buffering only if line is non-empty
                    if line.strip() == '':
                        print(f"Syntax error: {e}")
                        buf = []
                    # else keep buffering
                except SemanticError as e:
                    print(f"Type error: {e}")
                    buf = []
                except Exception as e:
                    print(f"Runtime error: {e}")
                    buf = []
                else:
                    buf = []


def main():
    if len(sys.argv) == 2:
        run_file(sys.argv[1])
    else:
        repl()


if __name__ == '__main__':
    main()
