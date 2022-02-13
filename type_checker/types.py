from dataclasses import dataclass


@dataclass
class TypeError(Exception):
    message: str


class Type:
    """Type base class"""


@dataclass
class Base(Type):
    """Class for base types

    Examples: Base('int'), Base('bool')
    """

    # type variables in System F
    name: str

    def __str__(self):
        return self.name


@dataclass
class Implication(Type):
    """Class for implication type

    Implication(left, right) corresponds term 'lambda <variable>:left. <term>' where term has type right"""

    left: Type
    right: Type

    def __str__(self):
        return f"({self.left}->{self.right})"

    def apply(self, other):
        """Get application's type result for terms with types self and other"""
        if self.left != other:
            raise TypeError(f"Type {self} can't be applied to type {other}.")
        return self.right


@dataclass
class Universal(Type):
    # forall <variable_name>. <inner>
    variable_name: str
    inner: Type

    def __str__(self):
        return f'(forall {self.variable_name}. {self.inner})'

def substitute(type, variable, new):
    if isinstance(type, Base):
        return new
    elif isinstance(type, Implication):
        return Implication(substitute(type.left, variable, new), substitute(type.right, variable, new))
    elif isinstance(type, Universal):
        if type.variable_name == variable.name:
            return type
        else:
            return Universal(type.variable_name, substitute(type.inner_term, variable, new))
    

class Context(dict):
    """class for contexts"""
