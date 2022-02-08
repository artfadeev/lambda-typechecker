from dataclasses import dataclass
from .types import Type, Base, Implication, Context

LAMBDA = 'L'



class TypedTerm:
    '''Typed term base class'''

    @classmethod
    def parse(cls, str_typed_term):
        # Assumption: correct syntax, no types outside lambda definitions
        operands = []
        current_operand = ''
        depth = 0

        for i, c in enumerate(str_typed_term):
            # lambda's scope reaches end of string
            if depth==0 and c==LAMBDA:
                operands.append(str_typed_term[i:])
                break
            elif depth==0 and (c.isalpha() or c=='('):
                current_operand = c
            elif depth>0:
                current_operand += c

            if c=='(':
                depth+=1
            elif c==')':
                depth-=1

            if depth==0 and current_operand:
                operands.append(current_operand)
                current_operand = ''

        if len(operands)==1 and str_typed_term.startswith('('):
            return cls.parse(str_typed_term[1:-1])
        elif len(operands)==1 and str_typed_term.isalpha():
            return Variable(str_typed_term)
        elif len(operands)==1 and str_typed_term.startswith(LAMBDA):
            binded_var, inside_term = str_typed_term[1:].split('.', 1)
            var_name, var_type = binded_var.split(':')
            return Abstraction(var_name, Type.parse(var_type), 
                                cls.parse(inside_term))
        elif len(operands)==2:
            return Application(cls.parse(operands[0]), cls.parse(operands[1]))


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
class Application(TypedTerm):
    left: TypedTerm
    right: TypedTerm

    def __str__(self):
        return f'({self.left} {self.right})'