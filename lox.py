import sys
from enum import Enum
from typing import List, Optional


class LoxSyntaxError(Exception):
    def __init__(self, line, message, where=""):
        self.line = line
        self.message = message
        self.where = where
        super().__init__()

    def __repr__(self):
        return f'[line {self.line}] Error{self.where}: {self.message}'


class TokenType(Enum):
  # Single-character tokens.
  LEFT_PAREN = 'LEFT_PAREN'
  RIGHT_PAREN = 'RIGHT_PAREN'
  LEFT_BRACE = 'LEFT_BRACE'
  RIGHT_BRACE = 'RIGHT_BRACE'

  COMMA = 'COMMA'
  DOT = 'DOT'
  MINUS = 'MINUS'
  PLUS = 'PLUS'
  SEMICOLON = 'SEMICOLON'
  SLASH = 'SLASH'
  STAR = 'STAR'

  # One or two character tokens.
  BANG = 'BANG'
  BANG_EQUAL = 'BANG_EQUAL'

  EQUAL = 'EQUAL'
  EQUAL_EQUAL = 'EQUAL_EQUAL'

  GREATER = 'GREATER'
  GREATER_EQUAL = 'GREATER_EQUAL'

  LESS = 'LESS'
  LESS_EQUAL = 'LESS_EQUAL'

  # Literals.
  IDENTIFIER = 'IDENTIFIER'
  STRING = 'STRING'
  NUMBER = 'NUMBER'

  # Keywords.
  AND = 'AND'
  CLASS = 'CLASS'
  ELSE = 'ELSE'
  FALSE = 'FALSE'
  FUN = 'FUN'
  FOR = 'FOR'
  IF = 'IF'
  NIL = 'NIL'
  OR = 'OR'

  PRINT = 'PRINT'
  RETURN = 'RETURN'
  SUPER = 'SUPER'
  THIS = 'THIS'
  TRUE = 'TRUE'
  VAR = 'VAR'
  WHILE = 'WHILE'

  EOF = 'EOF'


class Token:
    def __init__(self, type: TokenType, lexeme: str, literal: Optional[str], line: int):
        self.type = type
        self.lexeme = lexeme
        self.literal = literal
        self.line = line

    def __repr__(self):
        return f'{self.type} {self.lexeme} {self.literal}'


class Scanner:
    LEX_REGEXP = r'[a-zA-Z_][a-zA-Z_0-9]*'

    tokens: List[TokenType]

    start = 0
    current = 0
    line = 0

    def __init__(self, source_code: str):
        self.source_code = source_code
        self.tokens = []

    def scan_tokens(self) -> List[TokenType]:
        while not self.at_the_end:
            self.start = self.current
            self.scan_token()

        self.tokens.append(Token(TokenType.EOF, "", None, self.line))
        return self.tokens

    @property
    def at_the_end(self) -> bool:
        return self.current >= len(self.source_code)

    def scan_token(self):
        pass



def run_code(source_code):
    scanner = Scanner(source_code)
    tokens = scanner.scan_tokens()

    for token in tokens:
        print(token)


def run_file(path):
    with open(path, 'r') as file:
        code_lines = file.readlines()

    code = '\n'.join(code_lines)
    try:
        run_code(code)
    except LoxSyntaxError as error:
        print(error)
        exit(65)


def run_prompt():
    while True:
        try:
            run_code(input('>'))
        except LoxSyntaxError as error:
            print(error)


def run_lox():
    if len(sys.argv) >= 2:
        print("Usage: pylox [script]")
        exit(64)
    elif len(sys.argv) == 2:
        run_file(sys.argv[1])
    else:
        run_prompt()