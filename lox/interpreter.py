from lox.expr import ExprVisitor, Expr, BaseExpr
from lox.runtime_error import LoxRuntimeError
from lox.token import TokenType, Token
from lox.utils import noop


class Interpreter(ExprVisitor):
    def __init__(self, report_error=noop):
        self.report_error= report_error

    def interpret(self, expr: 'BaseExpr'):
        try:
            value = self.eval(expr)
            print(self.stringify(value))
        except LoxRuntimeError as error:
            self.report_error(error)

    def visit_binary(self, expr: 'Expr.Binary'):
        left = self.eval(expr.left)
        right = self.eval(expr.right)

        if expr.operator.type == TokenType.COMMA:
            self.eval(expr.left)
            return self.eval(expr.right)
        if expr.operator.type == TokenType.EQUAL_EQUAL:
            return self.is_equal(left, right)
        if expr.operator.type == TokenType.BANG_EQUAL:
            return not self.is_equal(left, right)
        if expr.operator.type == TokenType.LESS:
            return left < right
        if expr.operator.type == TokenType.LESS_EQUAL:
            return left <= right
        if expr.operator.type == TokenType.GREATER:
            return left > right
        if expr.operator.type == TokenType.GREATER_EQUAL:
            return left >= right
        if expr.operator.type == TokenType.PLUS:
            if isinstance(left, float) and isinstance(right, float):
                self.check_numbers(expr.operator, left, right)
                return left + right
            if isinstance(left, str) and isinstance(right, str):
                self.check_numbers(expr.operator, left, right)
                return left + right

            raise LoxRuntimeError(expr.operator, f"Cannot perform + on: {type(left)} + {type(right)}")
        if expr.operator.type == TokenType.MINUS:
            self.check_numbers(expr.operator, left, right)
            return left - right
        if expr.operator.type == TokenType.STAR:
            self.check_numbers(expr.operator, left, right)
            return left * right
        if expr.operator.type == TokenType.SLASH:
            self.check_numbers(expr.operator, left, right)
            return left / right

    def visit_ternary(self, expr: 'Expr.Ternary'):
        condition = self.eval(expr.condition)

        if condition:
            return self.eval(expr.left)
        return self.eval(expr.right)

    def visit_grouping(self, expr: 'Expr.Grouping'):
        return self.eval(expr.expression)

    def visit_literal(self, expr: 'Expr.Literal'):
        return expr.value

    def visit_unary(self, expr: 'Expr.Unary'):
        value = self.eval(expr.right)

        if expr.operator.type == TokenType.MINUS:
            self.check_number(expr.operator, value)
            return -value
        elif expr.operator.type == TokenType.BANG:
            return not self.is_truthy(value)
        return value

    def eval(self, expr: 'BaseExpr'):
        return expr.accept(self)

    def check_number(self, operator: Token, value):
        if isinstance(value, float):
            return

        raise LoxRuntimeError(operator, 'An operand must be a number.')

    def check_numbers(self, operator: Token, a, b):
        if not self.check_number(operator, a) or self.check_number(operator, b):
            return

        raise LoxRuntimeError(operator, 'Operands must be numbers.')

    def is_truthy(self, value):
        if isinstance(value, bool):
            return not value
        return True

    def is_equal(self, a, b):
        return a == b

    def stringify(self, value):
        if value is None:
            return 'nil'

        if isinstance(value, float):
            s = str(value)

            if s.endswith('.0'):
                return s[:-2]

            return s

        return str(value)