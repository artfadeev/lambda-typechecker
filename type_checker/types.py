from dataclasses import dataclass

class Type:
    '''Type base class'''


@dataclass
class Base(Type):
    # also for type variables in System F
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
            raise Exception(f'Type {self} can\'t be applied to type {other}!')
        return self.right


@dataclass
class Universal(Type):
    # forall <variable_name>. <inner>
    variable_name: str
    inner: Type

    def __str__(self):
        return f'(forall {self.variable_name}. {self.inner})'


class Context(dict):
    '''class for contexts'''