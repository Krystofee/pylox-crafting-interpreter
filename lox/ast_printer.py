from lox.expr import BaseExpr, Expr, ExprVisitor
from lox.token import Token, TokenType


class AstPrinter(ExprVisitor):
    def print(self, expr: BaseExpr):
        return expr.accept(self)

    def visit_unary(self, expr: Expr.Unary):
        return self.parenthesize(expr.operator.lexeme, expr.right)

    def visit_literal(self, expr: 'Expr.Literal'):
        return expr.value if expr.value is not None else 'nil'

    def visit_grouping(self, expr: 'Expr.Grouping'):
        return self.parenthesize('group', expr.expression)

    def visit_binary(self, expr: 'Expr.Binary'):
        return self.parenthesize(expr.operator.lexeme, expr.left, expr.right)

    def parenthesize(self, name, *exprs):
        return f'({name} {" ".join([str(x.accept(self)) for x in exprs])})'


def test_ast_printer():
    expr = Expr.Binary(
        Expr.Unary(Token(TokenType.PLUS, '+', None, 1), Expr.Literal(123)),
        Token(TokenType.STAR, '*', None, 1),
        Expr.Grouping(Expr.Literal(3.14)),
    )

    print(AstPrinter().print(expr))
