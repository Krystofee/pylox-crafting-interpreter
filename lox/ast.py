from enum import Enum


class Expr:
    class Type(Enum):
        BINARY = 'BINARY'
        GROUPING = 'GROUPING'
        LITERAL = 'LITERAL'
        UNARY = 'UNARY'

    def __init__(self, type: Type, *args):
        self.type = type
        self.args = args
