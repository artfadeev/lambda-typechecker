from dataclasses import dataclass

@dataclass
class TypeError(Exception):
    message: str

class Type:
    '''Type base class'''


@dataclass
class Base(Type):
    name: str

    def __str__(self):
        return self.name


@dataclass
class Implication(Type):
    left: Type
    right: Type

    def __str__(self):
        return f'({self.left}->{self.right})'

    def apply(self, other):
        if self.left!=other:
            raise TypeError(f'Type {self} can\'t be applied to type {other}.')
        return self.right



class Context(dict):
    '''class for contexts'''