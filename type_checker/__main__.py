import argparse

from .types import Type, Context
from .terms import TypedTerm
from .type_checker import type_check
from .parser import Scanner, Parser, parse_context, ScanError, SyntaxError

cli_parser = argparse.ArgumentParser(
    description='Simply typed lambda calculus type checker')

cli_parser.add_argument('source', type=str, 
    help='term to check')
cli_parser.add_argument('--context', dest='context', default='', type=str,
    help='context (default is empty)')

args = cli_parser.parse_args()

context = parse_context(args.context)
source = args.source

try:
    tokens = Scanner(source).scan()
except ScanError as exc:
    print(source)
    print(' '*exc.position+'^')
    print("Scan Error:", exc.message)
    exit()

try:
    term = Parser(tokens).parse()
except SyntaxError as exc:
    print(source)
    print(' '*exc.position+'^')
    print("Parse error:", exc.message)
    exit()

try:
    _type = type_check(term, context)
except Exception:
    print('Type check unsuccessful')
else:
    print('Type check successful')
    print(f'Term\'s type {str(_type)}')
