from .types import Type, Context
from .terms import TypedTerm
from .type_checker import type_check

if __name__=='__main__':
    str_context = input('Context: ')
    str_term = input('Term: ')

    context = Context.parse(str_context)
    term = TypedTerm.parse(str_term)

    try:
        _type = type_check(term, context)
    except Exception:
        print('Type check unsuccessful')
    else:
        print('Type check successful')
        print(f'Term\'s type {str(_type)}')
