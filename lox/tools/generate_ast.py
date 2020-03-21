class_declaration = [
    "Binary   - left: BaseExpr, operator: Token, right: BaseExpr",
    "Grouping - expression: BaseExpr",
    "Literal  - value: object",
    "Unary    - operator: Token, right: BaseExpr"
]

BASE_CLASS = """from lox.token import Token


class BaseExpr:
    def accept(self, visitor: 'ExprVisitor'):
        raise NotImplementedError
        
"""


def prepend_undescore(c: str):
    return '_' + c


def char_to_snake(c: str):
    return prepend_undescore(c.lower()) if c.isupper() else c


def to_snake_case(source, result=''):
    return to_snake_case(source[1:], result + char_to_snake(source[0])) if source else result


def generate_class(name, args):
    nl = '\n'
    tab = '    '
    cls = f'''    class {name}(BaseExpr):
        def __init__(self, {','.join(args)}):
            {f"{nl}{tab}{tab}{tab}".join([f"self.{x.split(':')[0]} = {x.split(':')[0]}" for x in args])}
            
        def accept(self, visitor: 'ExprVisitor'):
            return visitor.visit{to_snake_case(name)}(self)
'''
    return cls


def generate_classes():
    result = '''class Expr(BaseExpr):
'''

    for cls in class_declaration:
        cls_name, cls_args = cls.split('-')
        cls_name, cls_args = cls_name.strip(), cls_args.strip().split(',')
        result += (generate_class(cls_name, cls_args)) + '\n'

    return result + '\n'


def generate_visitor():
    result = '''class ExprVisitor:'''
    for cls in class_declaration:
        cls_name, cls_args = cls.split('-')
        cls_name = cls_name.strip()

        result += f'''    
    def visit{to_snake_case(cls_name)}(self, expr: 'Expr.{cls_name}'):
        raise NotImplementedError()
        '''

    return result


if __name__ == '__main__':
    with open('expr.py', 'w') as file:
        file.write(BASE_CLASS)
        file.write(generate_classes())
        file.write(generate_visitor())
