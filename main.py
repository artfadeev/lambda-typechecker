class Type:
    def __init__(self, rule, *args): 
        self.rule = rule
        self.args = args

    @classmethod
    def implication(cls, left, right):
        '''Constructor for Type::=Type->Type '''
        return cls('implication', left, right)

    @classmethod
    def base(cls, base_variable):
        '''Constructor for Type::=Base'''
        return cls('base', base_variable)

    def __eq__(self, other):
        if self.rule != other.rule:
            return False

        for (t1, t2) in zip(self.args, other.args):
            if t1!=t2:
                return False
        
        return True

    def __str__(self):
        if self.rule == 'base':
            return self.args[0]
        else:
            return f'({str(self.args[0])}->{str(self.args[1])})'

    def __repr__(self):
        if len(self.args)==2:
            return f'implication({self.args[0].__repr__()}, {self.args[1].__repr__()})'
        else:
            return f'base({self.args[0]})'

def parse_type(str_type):
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
        return Type.implication(parse_type(operands[0]), 
                                parse_type(operands[1]))
    elif len(operands)==1 and operands[0].isalpha():
        return Type.base(operands[0])
    else:
        return parse_type(str_type[1:-1])
