from enum import Enum
from dataclasses import dataclass
from .types import Base, Implication, Context
from .terms import Variable, Application, Abstraction

class TokenType(Enum):
    LAMBDA = 1
    COLON = 2
    DOT = 3
    BRACKET_OPEN = 4
    BRACKET_CLOSE = 5
    VARIABLE = 6
    ARROW = 7

single_character_tokens = {
    ':': TokenType.COLON,
    '.': TokenType.DOT,
    '(': TokenType.BRACKET_OPEN,
    ')': TokenType.BRACKET_CLOSE,
}

keywords = {
    'lambda': TokenType.LAMBDA,
}

@dataclass
class Token:
    type: TokenType
    lexeme: str 
    position: int # position of first symbol in the source string


@dataclass
class ScanError(Exception):
    message: str
    position: int

    def __str__(self):
        return f'ScanError at position {self.position}: {self.message}'

@dataclass
class SyntaxError(Exception):
    message: str
    position: int


class Scanner:
    '''Class for tokenizing input'''
    def __init__(self, source: str):
        self.source = source+'\n' # newline is to avoid string's end
        self.position = 0

    def _word(self):
        '''scan word (variable/keyword) starting at self.position'''
        start = self.position

        while self.source[self.position].isalpha():
            self.position += 1

        return self.source[start:self.position]

    def scan(self):
        tokens = []

        while (self.position<len(self.source)):
            c = self.source[self.position]

            # whitespace
            if c in (' ', '\n', '\t'):
                self.position += 1
            # :.()
            elif c in single_character_tokens.keys():
                tokens.append(Token(single_character_tokens[c],
                                    c,
                                    self.position))
                self.position += 1
            # arrow
            elif self.source[self.position:self.position+2] == '->':
                tokens.append(Token(TokenType.ARROW, '->', self.position))
                self.position += 2
            # keywords and variables
            elif c.isalpha():
                pos = self.position
                word = self._word()

                if word in keywords.keys():
                    tokens.append(Token(keywords[word], word, pos))
                else:
                    tokens.append(Token(TokenType.VARIABLE, word, pos))
            else:
                raise ScanError('Unknown token', self.position)

        return tokens

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.position = 0

        # position of last symbol of the source string for error messages
        if len(self.tokens)==0:
            self.last_position = 0
        else:
            self.last_position = self.tokens[-1].position + \
                                 len(self.tokens[-1].lexeme)

    def end(self):
        return self.position>=len(self.tokens)

    def current(self):
        return self.tokens[self.position]

    def read(self, *expected, move=True):
        '''Read one token of expected TokenTypes. Else raise exception'''
        if self.end():
            raise SyntaxError(f"Expected {expected}, got end of source", 
                              self.last_position)

        current = self.current()
        if current.type not in expected:
            raise SyntaxError(f"Expected {' or '.join(map(str, expected))}, "+\
                                "got {self.current()}", current.position)
        if move:
            self.position += 1
        return current

    def _primary_type(self):
        token = self.read(TokenType.VARIABLE, TokenType.BRACKET_OPEN)

        if token.type == TokenType.VARIABLE:
            return Base(token.lexeme)
        elif token.type == TokenType.BRACKET_OPEN:
            opening_bracket_position = token.position
            term = self._type()
            self.read(TokenType.BRACKET_CLOSE)
            return term

    def _type(self):
        term = self._primary_type()

        if not self.end() and self.current().type==TokenType.ARROW:
            self.position+=1
            term_to = self._type()
            return Implication(term, term_to)

        return term

    def _lambda(self):
        self.read(TokenType.LAMBDA)
        variable_name = self.read(TokenType.VARIABLE).lexeme
        self.read(TokenType.COLON)
        variable_type = self._type()
        self.read(TokenType.DOT)
        inner_term = self._application()

        return Abstraction(variable_name, variable_type, inner_term)

    def _primary_term(self):
        token = self.read(TokenType.VARIABLE, TokenType.BRACKET_OPEN,
                            TokenType.LAMBDA, move=False)
        if token.type == TokenType.VARIABLE:
            # TODO: add self._variable?
            self.position += 1
            return Variable(token.lexeme)
        elif token.type == TokenType.BRACKET_OPEN:
            self.position += 1
            term = self._application()
            self.read(TokenType.BRACKET_CLOSE)
            return term
        elif token.type == TokenType.LAMBDA:
            return self._lambda()

    def _application(self):
        term = self._primary_term()
        while not self.end() and self.current().type in \
            (TokenType.VARIABLE, TokenType.BRACKET_OPEN, TokenType.LAMBDA):
            term = Application(term, self._primary_term())

        return term

    def parse(self):
        term = self._application()

        if not self.end():
            # something like "<primary term> ... <primary term> )"
            raise SyntaxError("Unknown syntax", self.current().position)
        return term


def parse_context(str_context):
    '''Parse context from string in form var1:type1, var2:type2, ...
    
    If variables repeat, latest value will be taken'''

    # Assumptions: correct syntax
    if str_context=='':
        return Context({})

    context = {}
    definitions = map(lambda d: d.strip().split(':'),
                      str_context.split(','))
    for (var, str_type) in definitions:
        context[var] = Parser(Scanner(str_type).scan())._type()
    return Context(context)