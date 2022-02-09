from enum import Enum
from dataclasses import dataclass

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
