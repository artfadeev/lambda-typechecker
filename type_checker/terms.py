from dataclasses import dataclass
from .types import Type, Base, Implication, Context


class TypedTerm:
    """Typed term base class"""


@dataclass
class Variable(TypedTerm):
    """Class for typed term consisting of just variable"""

    name: str

    def __str__(self):
        return self.name


@dataclass
class Abstraction(TypedTerm):
    """Class for abstraction typed terms

    Example: Abstraction("x", Base("a"), Variable("x")) corresponds to
        identity function of type a: 'lambda x:a. x'"""

    variable_name: str
    variable_type: Type
    inner_term: TypedTerm

    def __str__(self):
        return (
            f"(lambda {self.variable_name}:"
            + f"{self.variable_type}.{self.inner_term})"
        )


@dataclass
class Application(TypedTerm):
    """Class for application typed terms

    Example: Application(Variable("x"), Variable("y")) corresponds to term
        'x y'"""

    left: TypedTerm
    right: TypedTerm

    def __str__(self):
        return f"({self.left} {self.right})"
