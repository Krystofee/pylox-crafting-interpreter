from typing import List

from lox.expr import BaseExpr, Expr
from lox.token import Token, TokenType
from lox.utils import noop


class Parser:
    current = 0

    class ParseError(Exception):
        def __init__(self, token: Token, message: str):
            self.token = token
            self.message = message

    def __init__(self, tokens: List[Token], report_error = noop):
        self.tokens = tokens
        self.report_error = report_error

    def parse(self):
        try:
            return self.expression()
        except self.ParseError:
            return

    def expression(self) -> BaseExpr:
        return self.comma()

    def comma(self) -> BaseExpr:
        expr = self.ternary()
        while self.match(TokenType.COMMA):
            operator = self.previous()
            expr = Expr.Binary(expr, operator, self.expression())
        return expr

    def ternary(self):
        expr = self.equality()

        if self.peek().type == TokenType.QUESTION:
            self.advance()
            left = self.expression()
            if self.match(TokenType.COLON):
                right = self.expression()
                return Expr.Ternary(expr, left, right)

            raise self.error(self.peek(), 'Unterminated ternary operator. Expected colon.')

        return expr


    def equality(self) -> BaseExpr:
        expr = self.comparison()

        while self.match(TokenType.BANG_EQUAL, TokenType.EQUAL_EQUAL):
            operator = self.previous()
            right = self.comparison()
            expr = Expr.Binary(expr, operator, right)

        return expr

    def comparison(self) -> BaseExpr:
        expr = self.addition()

        while self.match(TokenType.LESS, TokenType.GREATER, TokenType.LESS_EQUAL, TokenType.GREATER_EQUAL):
            operator = self.previous()
            right = self.addition()
            expr = Expr.Binary(expr, operator, right)

        return expr

    def addition(self) -> BaseExpr:
        expr = self.multiplication()

        while self.match(TokenType.PLUS, TokenType.MINUS):
            operator = self.previous()
            right = self.multiplication()
            expr = Expr.Binary(expr, operator, right)

        return expr

    def multiplication(self) -> BaseExpr:
        expr = self.unary()

        while self.match(TokenType.STAR, TokenType.SLASH):
            operator = self.previous()
            right = self.unary()
            expr = Expr.Binary(expr, operator, right)

        return expr

    def unary(self) -> BaseExpr:
        if self.match(TokenType.MINUS, TokenType.BANG):
            operator = self.previous()
            right = self.unary()
            return Expr.Unary(operator, right)
        return self.primary()

    def primary(self) -> BaseExpr:
        if self.match(TokenType.NUMBER):
            return Expr.Literal(self.previous().literal)
        elif self.match(TokenType.STRING):
            return Expr.Literal(self.previous().literal)
        elif self.match(TokenType.TRUE):
            return Expr.Literal(True)
        elif self.match(TokenType.FALSE):
            return Expr.Literal(False)
        elif self.match(TokenType.NIL):
            return Expr.Literal(None)

        if self.match(TokenType.LEFT_PAREN):
            expr = self.expression()
            if not self.consume('Expected right paren ")" after expression.', TokenType.RIGHT_PAREN):
                pass
            return Expr.Grouping(expr)

        raise self.error(self.peek(), 'Expected expression.')

    @property
    def at_the_end(self):
        return self.peek().type == TokenType.EOF

    def check(self, token_type: TokenType):
        return self.peek().type == token_type if not self.at_the_end else False

    def advance(self):
        if not self.at_the_end:
            self.current += 1
        return self.previous()

    def match(self, *token_types: TokenType):
        return any([self.check(token_type) and self.advance() for token_type in token_types])

    def peek(self) -> Token:
        return self.tokens[self.current]

    def previous(self) -> Token:
        return self.tokens[self.current - 1]

    def consume(self, message: str, token_type: TokenType):
        if not self.match(token_type):
            raise self.error(self.peek(), message)

    def error(self, token: Token, message: str):
        self.report_error(token, message)
        return self.ParseError(token, message)

    def synchronize(self):
        self.advance()

        while not self.at_the_end:
            if self.previous().type == TokenType.SEMICOLON:
                return
            elif (
                    self.peek().type == TokenType.CLASS
                    or self.peek().type == TokenType.FUN
                    or self.peek().type == TokenType.FOR
                    or self.peek().type == TokenType.VAR
                    or self.peek().type == TokenType.IF
                    or self.peek().type == TokenType.WHILE
                    or self.peek().type == TokenType.PRINT
                    or self.peek().type == TokenType.RETURN
            ):
                self.advance()
