from dataclasses import dataclass
from .types import Type, Implication, Context, Universal, substitute
from .terms import TypedTerm, Variable, Application, Abstraction, TypeApplication, TypeAbstraction


@dataclass
class UnknownVariableError(Exception):
    message: str


def type_check(term, context=None, type_variables=None):
    if context is None:
        context = Context({})
    if type_variables is None:
        type_variables = set()

    if isinstance(term, Variable):
        if term.name not in context.keys():
            raise UnknownVariableError(
                f"Variable {term.name} lacks type in given context."
            )
        return context[term.name]
    elif isinstance(term, Abstraction):
        inner_context = context.copy()
        inner_context[term.variable_name] = term.variable_type
        return Implication(
            term.variable_type, type_check(term.inner_term, inner_context, type_variables)
        )
    elif isinstance(term, Application):
        return type_check(term.left, context, type_variables).apply(
            type_check(term.right, context, type_variables)
        )
    elif isinstance(term, TypeAbstraction):
        return Universal(term.variable_name, type_check(term.inner_term, context, type_variables))
    elif isinstance(term, TypeApplication):
        if not isinstance(term, TypeAbstraction):
            raise TypeError(f"Term {term.left} can't be applied to type.")
        new_type_variables = type_variables
        new_type_variables.add(term.left.variable_name)

        # should be universal
        left_type = type_check(term.left, context, new_type_variables)
        return substitute(left_type.inner, Variable(term.left.variable_name),
            term.right)
