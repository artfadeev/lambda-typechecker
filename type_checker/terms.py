from dataclasses import dataclass
from .types import Type, Base, Implication, Context

LAMBDA = 'lambda '
TYPE_LAMBDA = 'type_lambda '

class TypedTerm:
    '''Typed term base class'''


@dataclass
class Variable(TypedTerm):
    name: str

    def __str__(self):
        return self.name


@dataclass
class Abstraction(TypedTerm):
    variable_name: str
    variable_type: Type
    inner_term: TypedTerm

    def __str__(self):
        return f'({LAMBDA}{self.variable_name}:'+\
                f'{self.variable_type}.{self.inner_term})'


@dataclass
class TypeAbstraction(TypedTerm):
    variable_name: str
    inner_term: TypedTerm

    def __str__(self):
        return f'{TYPE_LAMBDA}{self.variable_name}.{self.inner_term}'


@dataclass
class Application(TypedTerm):
    left: TypedTerm
    right: TypedTerm

    def __str__(self):
        return f'({self.left} {self.right})'

@dataclass
class TypeApplication(TypedTerm):
    left: TypedTerm
    right: Type

    def __str__(self):
        return f'({self.left} [{self.right}])'