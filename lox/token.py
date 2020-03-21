from enum import Enum
from typing import Optional


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
    def __init__(self, type: TokenType, lexeme: str, literal: Optional[object], line: int):
        self.type = type
        self.lexeme = lexeme
        self.literal = literal
        self.line = line

    def __str__(self):
        return self.lexeme

    def __repr__(self):
        return f'<{self.type} {self.lexeme} {self.literal}>'