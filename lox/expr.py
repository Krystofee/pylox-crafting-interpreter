from lox.token import Token


class BaseExpr:
    def accept(self, visitor: 'ExprVisitor'):
        raise NotImplementedError
        
class Expr(BaseExpr):
    class Binary(BaseExpr):
        def __init__(self, left: BaseExpr, operator: Token, right: BaseExpr):
            self.left = left
            self. operator =  operator
            self. right =  right
            
        def accept(self, visitor: 'ExprVisitor'):
            return visitor.visit_binary(self)

    class Grouping(BaseExpr):
        def __init__(self, expression: BaseExpr):
            self.expression = expression
            
        def accept(self, visitor: 'ExprVisitor'):
            return visitor.visit_grouping(self)

    class Literal(BaseExpr):
        def __init__(self, value: object):
            self.value = value
            
        def accept(self, visitor: 'ExprVisitor'):
            return visitor.visit_literal(self)

    class Unary(BaseExpr):
        def __init__(self, operator: Token, right: BaseExpr):
            self.operator = operator
            self. right =  right
            
        def accept(self, visitor: 'ExprVisitor'):
            return visitor.visit_unary(self)


class ExprVisitor:    
    def visit_binary(self, expr: 'Expr.Binary'):
        raise NotImplementedError()
            
    def visit_grouping(self, expr: 'Expr.Grouping'):
        raise NotImplementedError()
            
    def visit_literal(self, expr: 'Expr.Literal'):
        raise NotImplementedError()
            
    def visit_unary(self, expr: 'Expr.Unary'):
        raise NotImplementedError()
        