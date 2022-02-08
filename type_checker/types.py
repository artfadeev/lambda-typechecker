from dataclasses import dataclass
LAMBDA = 'L'


class Type:
    '''Type base class'''

    @classmethod
    def parse(cls, str_type):
        '''Define type from string representation'''
        
        # Assumption: str_type is either (str_type->str_type) or base (one letter)
        # TODO: check for incorrect syntax.
        # TODO: make some brackets unnecessary

        depth = 0 # depth of nested brackets
        operands = []
        current_operand = ''

        for c in str_type:
            # 1. Modify current top-level operand

            # starting new operand
            if depth==0 and (c.isalpha() or c=='('):
                current_operand = c
            # continuing existing operand
            elif depth>0:
                current_operand += c # FIX: quadratic complexity

            # 2. Change depth
            if c=='(':
                depth+=1
            elif c==')':
                depth-=1

            # 3. Finish top-level operand
            if depth==0 and current_operand:
                operands.append(current_operand)
                current_operand = '' # unnecessary line
        
        if len(operands)==2:
            return Implication(cls.parse(operands[0]), cls.parse(operands[1]))
        elif len(operands)==1 and operands[0].isalpha():
            return Base(operands[0])
        else:
            return cls.parse(str_type[1:-1])


@dataclass
class Base(Type):
    name: str

    def __str__(self):
        return self.name

    def __repr__(self):
        return f'Base({self.name})'


@dataclass
class Implication(Type):
    left: Type
    right: Type

    def __str__(self):
        return f'({self.left}->{self.right})'

    def __repr__(self):
        return f'Implication({repr(self.left)}, {repr(self.right)})'

    def apply(self, other):
        if self.left!=other:
            raise Exception(f'Type {self} can\'t be applied to type {other}!')
        return self.right



class Context(dict):
    @classmethod
    def parse(cls, str_context):
        '''Parse context from string in form var1:type1, var2:type2, ...
        
        If variables repeat, latest value will be taken'''

        # Assumptions: correct syntax
        if str_context=='':
            return cls({})

        context = {}
        definitions = map(lambda d: d.strip().split(':'),
                          str_context.split(','))
        for (var, str_type) in definitions:
            context[var] = Type.parse(str_type)
        return cls(context)