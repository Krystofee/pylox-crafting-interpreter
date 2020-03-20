class_declaration = [
    "Binary   - left: Expr, operator: Token, right: Expr",
    "Grouping - expression: Expr",
    "Literal  - value: object",
    "Unary    - operator: Token, right: Expr"
]

BASE_CLASS = """from token import Token


class Expr:
    def accept(self, visitor: 'ExprVisitor'):
        raise NotImplementedError
        
"""



def generate_class(name, args):
    nl = '\n'
    tab = '    '
    cls = f'''class {name}(Expr):
    def __init__(self, {','.join(args)}):
        {f"{nl}{tab}{tab}".join([f"self.{x.split(':')[0]} = {x.split(':')[0]}" for x in args])}
        
    def accept(self, visitor: 'ExprVisitor'):
        return visitor.visit{name}Expr(self)
'''
    return cls


def generate_classes():
    result = ''

    for cls in class_declaration:
        cls_name, cls_args = cls.split('-')
        cls_name, cls_args = cls_name.strip(), cls_args.strip().split(',')

        result += ('\n')
        result += ('\n')

        result += (generate_class(cls_name, cls_args))

    result += ('\n')
    result += ('\n')

    for cls in class_declaration:
        cls_name, cls_args = cls.split('-')
        cls_name = cls_name.strip()

        result += (f'Expr.{cls_name} = {cls_name}\n')

    return result


def generate_visitor():
    result = '''
class ExprVisitor:
'''
    for cls in class_declaration:
        cls_name, cls_args = cls.split('-')
        cls_name = cls_name.strip()

        result += f'''
    def visit{cls_name}Expr(self, expr: '{cls_name}'):
        raise NotImplementedError()
        '''

    return result


if __name__ == '__main__':
    with open('expr.py', 'w') as file:
        file.write(BASE_CLASS)
        file.write(generate_visitor())
        file.write(generate_classes())
