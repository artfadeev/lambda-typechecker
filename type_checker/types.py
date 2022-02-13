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


class Context(dict):
    """class for contexts"""
