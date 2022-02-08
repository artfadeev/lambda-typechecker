from .types import Type, Context
from .terms import TypedTerm

LAMBDA = 'L' # symbol for \lambda


def type_check(term, context = None):
    if context is None:
        context = Context({})
    if term.rule=='variable':
        name = term.args[0] # ugly!
        if name not in context.keys():
            raise Exception(f'{name} lacks type in given context')
        return context[name]
    elif term.rule=='abstraction':
        binded_var, inner_term = term.args
        inner_context = context.copy()
        inner_context[binded_var.args[0]] = binded_var.type
        return Type.implication(binded_var.type,
                                type_check(inner_term, inner_context))
    elif term.rule=='application':
        return type_check(term.args[0], context).apply(
                type_check(term.args[1], context))