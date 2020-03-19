from typing import List


class Expr:
    __init_args: List[str]

    Binary: 'Expr'
    Grouping: 'Expr'
    Literal: 'Expr'
    Unary: 'Expr'

    def __init__(self, *args)
        for name, value in zip(self.__init_args, args):
            setattr(self, name, value)

    @staticmethod
    def create_class(name, *args):
        setattr(Expr, name, type(name, (Expr,), {'__init_args': args}))


Expr.create_class('Binary', 'left', 'operator', 'right')
Expr.create_class('Grouping', 'expression')
Expr.create_class('Literal', 'value')
Expr.create_class('Unary', 'operator', 'right')
