from typing import List

from token import TokenType, Token
from utils import noop


class Scanner:
    tokens: List[TokenType]

    start = 0
    current = 0
    line = 1

    def __init__(self, source_code: str, report_error=noop):
        self.source_code = source_code
        self.report_error = report_error
        self.tokens = []
        self.keywords = {
            'and': TokenType.AND,
            'class': TokenType.CLASS,
            'else': TokenType.ELSE,
            'false': TokenType.FALSE,
            'for': TokenType.FOR,
            'fun': TokenType.FUN,
            'if': TokenType.IF,
            'nil': TokenType.NIL,
            'or': TokenType.OR,
            'print': TokenType.PRINT,
            'return': TokenType.RETURN,
            'super': TokenType.SUPER,
            'this': TokenType.THIS,
            'true': TokenType.TRUE,
            'var': TokenType.VAR,
            'while': TokenType.WHILE,
        }

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
        c = self.advance()
        if c == '(': self.add_token(TokenType.LEFT_PAREN)
        elif c == ')': self.add_token(TokenType.RIGHT_PAREN)
        elif c == '{': self.add_token(TokenType.LEFT_BRACE)
        elif c == '}': self.add_token(TokenType.RIGHT_BRACE)
        elif c == ',': self.add_token(TokenType.COMMA)
        elif c == '.': self.add_token(TokenType.DOT)
        elif c == '-': self.add_token(TokenType.MINUS)
        elif c == '+': self.add_token(TokenType.PLUS)
        elif c == ';': self.add_token(TokenType.SEMICOLON)
        elif c == '*': self.add_token(TokenType.STAR)
        elif c == '!': self.add_token(TokenType.BANG_EQUAL) if self.match('=') else self.add_token(TokenType.BANG)
        elif c == '=': self.add_token(TokenType.EQUAL_EQUAL) if self.match('=') else self.add_token(TokenType.EQUAL)
        elif c == '<': self.add_token(TokenType.LESS_EQUAL) if self.match('=') else self.add_token(TokenType.LESS)
        elif c == '>': self.add_token(TokenType.GREATER_EQUAL) if self.match('=') else self.add_token(TokenType.GREATER)
        elif c == '/':
            if self.match('/'):
                while self.peek() != '\n' and not self.at_the_end:
                    self.advance()
            elif self.match('*'):
                while not (self.peek() == '*' and self.peek_next() == '/') and not self.at_the_end:
                    if self.peek() == '\n':
                        self.line += 1
                    self.advance()

                if self.at_the_end:
                    self.report_error(self.line, "Unterminated comment")
                else:
                    self.advance()
                    self.advance()
            else:
                self.add_token(TokenType.SLASH)
        elif c == ' ': pass
        elif c == '\r': pass
        elif c == '\t': pass
        elif c == '\n':
            self.line += 1
        elif c == '"': self.string()
        elif self.is_digit(c):
            self.number()
        elif self.is_alpha(c):
            self.identifier()
        else:
            self.report_error(self.line, "Unexpected chracter.")

    def string(self):
        while self.peek() != '"' and not self.at_the_end:
            if self.peek() == '\n': self.line += 1
            self.advance()

        if self.at_the_end:
            self.report_error(self.line, "Unterminated string")
            return

        self.advance()

        value = self.source_code[self.start + 1:self.current - 1]
        self.add_token(TokenType.STRING, value)

    def number(self):
        while self.is_digit(self.peek()):
            self.advance()

        if self.peek() == '.' and self.is_digit(self.peek_next()):
            self.advance()

            while self.is_digit(self.peek()):
                self.advance()

        value = self.source_code[self.start:self.current]
        self.add_token(TokenType.NUMBER, float(value))

    def identifier(self):
        while self.is_alpha_numeric(self.peek()):
            self.advance()

        text = self.source_code[self.start:self.current]
        type = self.keywords.get(text, TokenType.IDENTIFIER)
        self.add_token(type)

    def add_token(self, type: TokenType, literal = None):
        text = self.source_code[self.start:self.current]
        self.tokens.append(Token(type, text, literal, self.line))

    def advance(self):
        self.current += 1
        return self.source_code[self.current - 1]

    def match(self, expected: str):
        if self.at_the_end:
            return False

        if self.source_code[self.current] != expected:
            return False

        self.current += 1
        return True

    def peek(self):
        if self.at_the_end:
            return '\0'
        return self.source_code[self.current]

    def peek_next(self):
        if self.current + 1 >= len(self.source_code):
            return '\0'
        return self.source_code[self.current + 1]

    def is_alpha(self, char: str):
        return char >= 'a' and char <= 'z' or char >= 'A' and char <= 'Z' or char == '_'

    def is_digit(self, char: str):
        return char >= '0' and char <= '9'

    def is_alpha_numeric(self, char: str):
        return self.is_digit(char) or self.is_alpha(char)