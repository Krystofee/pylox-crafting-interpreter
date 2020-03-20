from lox.expr import ExprVisitor, Unary, Literal, Grouping, Binary, Expr
from lox.token import TokenType, Token


class AstPrinter(ExprVisitor):
    def print(self, expr: Expr):
        return expr.accept(self)

    def visitUnaryExpr(self, expr: 'Unary'):
        return self.parenthesize(expr.operator.lexeme, expr.right)

    def visitLiteralExpr(self, expr: 'Literal'):
        return expr.value if expr.value is not None else 'nil'

    def visitGroupingExpr(self, expr: 'Grouping'):
        return self.parenthesize('group', expr.expression)

    def visitBinaryExpr(self, expr: 'Binary'):
        return self.parenthesize(expr.operator.lexeme, expr.left, expr.right)

    def parenthesize(self, name, *exprs):
        return f'({name} {" ".join([str(x.accept(self)) for x in exprs])})'


def test_ast_printer():
    expr = Binary(
        Unary(Token(TokenType.PLUS, '+', None, 1), Literal(123)),
        Token(TokenType.STAR, '*', None, 1),
        Grouping(Literal(3.14)),
    )

    print(AstPrinter().print(expr))
