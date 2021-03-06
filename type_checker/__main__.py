import argparse

from .types import Type, Context, TypeError
from .terms import TypedTerm
from .type_checker import type_check, UnknownVariableError
from .parser import Scanner, Parser, parse_context, ScanError, SyntaxError

cli_parser = argparse.ArgumentParser(
    description="Simply typed lambda calculus type checker"
)

cli_parser.add_argument("source", type=str, help="term to check")
cli_parser.add_argument(
    "--context",
    dest="context",
    default="",
    type=str,
    help="context (default is empty)",
)

args = cli_parser.parse_args()

try:
    context = parse_context(args.context)
except Exception:
    print("Context syntax is incorrect")
    exit()

source = args.source

try:
    tokens = Scanner(source).scan()
except ScanError as exc:
    print(source)
    print(" " * exc.position + "^")
    print("Scan Error:", exc.message)
    exit()

try:
    term = Parser(tokens).parse()
except SyntaxError as exc:
    print(source)
    print(" " * exc.position + "^")
    print("Parse error:", exc.message)
    exit()

try:
    _type = type_check(term, context)
except TypeError as exc:
    print("Type error: " + exc.message)
except UnknownVariableError as exc:
    print(exc.message)
else:
    print("Type check successful")
    print(f"Term's type {str(_type)}")
