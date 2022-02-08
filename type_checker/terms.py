from .types import Type, Context

LAMBDA = 'L'


class TypedTerm:
    def __init__(self, rule, *args, _type=None):
        '''Initialize 

        Arguments:
        rule - either 'variable', 'abstraction' or 'application'
        args - arguments: 1 for variable, 2 for abstraction, 2 for application
        _type -- expected type of the term. Default is None.
        '''

        # TODO: in 'variable' case str shouldn't be stored in args.
        #       create another argument?
        self.rule = rule
        self.args = args
        self.type = _type

    @classmethod
    def variable(cls, name, _type=None):
        return cls('variable', name, _type=_type)

    @classmethod
    def abstraction(cls, binded_var, term, _type=None):
        if binded_var.rule != 'variable':
            # TODO: create good exception names
            raise Exception('Lambda parameter must be a variable.')
        # TODO: maybe this check should be performed while typecheking?
        if binded_var.type is None:
            raise Exception('Lambda parameter must have a type.') 
        return cls('abstraction', binded_var, term, _type=_type)

    @classmethod
    def application(cls, left_term, right_term, _type=None):
        return cls('application', left_term, right_term, _type=_type)


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
            return cls.variable(str_typed_term)
        elif len(operands)==1 and str_typed_term.startswith(LAMBDA):
            binded_var, inside_term = str_typed_term[1:].split('.', 1)
            var_name, var_type = binded_var.split(':')
            return cls.abstraction(
                        cls.variable(var_name, Type.parse(var_type)),
                        cls.parse(inside_term)
                        )
        elif len(operands)==2:
            return cls.application(
                        cls.parse(operands[0]),
                        cls.parse(operands[1])
                        )

    def __str__(self):
        s = ''

        # term
        if self.rule=='variable':
            s = self.args[0]
        elif self.rule=='abstraction':
            s = f'({LAMBDA}{str(self.args[0])}.{str(self.args[1])})'
        elif self.rule=='application':
            s = f'({str(self.args[0])} {str(self.args[1])})'

        # type (if given)
        if self.type is not None:
            s += f':{str(self.type)}'
        return s

    def __eq__(self, other):
        if self.rule!=other.rule or \
           self.type!=other.type or \
           len(self.args)!=len(other.args):
            return False

        for arg1, arg2 in zip(self.args, other.args):
            if arg1!=arg2:
                return False

        return True
