from .types import Type, Context
from .terms import TypedTerm
from .type_checker import type_check
from .parser import Scanner, Parser, parse_context, ScanError, SyntaxError

if __name__=='__main__':
    str_context = input('Context: ')
    str_term = input('Term: ')

    context = parse_context(str_context)
    try:
        tokens = Scanner(str_term).scan()
    except ScanError as exc:
        print(str_term)
        print(' '*exc.position+'^')
        print("Scan Error: "+exc.message)
        exit()

    try:
        term = Parser(tokens).parse()
    except SyntaxError as exc:
        print(exc.message)
        exit()

    try:
        _type = type_check(term, context)
    except Exception:
        print('Type check unsuccessful')
    else:
        print('Type check successful')
        print(f'Term\'s type {str(_type)}')
