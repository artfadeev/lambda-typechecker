from .types import Type, Implication, Context
from .terms import TypedTerm, Variable, Application, Abstraction

LAMBDA = 'L' # symbol for \lambda


def type_check(term, context=None):
    if context is None:
        context = Context({})

    if isinstance(term, Variable):
        if term.name not in context.keys():
            raise Exception(f'{term.name} lacks type in given context!')
        return context[term.name]
    elif isinstance(term, Abstraction):
        inner_context = context.copy()
        inner_context[term.variable_name] = term.variable_type
        return Implication(term.variable_type,
                            type_check(term.inner_term, inner_context))
    elif isinstance(term, Application):
        return type_check(term.left, context).apply(
                type_check(term.right, context))