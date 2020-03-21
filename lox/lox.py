import sys

from lox.ast_printer import AstPrinter
from lox.parser import Parser
from lox.scanner import Scanner
from lox.token import Token, TokenType


class Lox:
    has_error = False

    def run_code(self, source_code):
        scanner = Scanner(source_code, self.error)
        tokens = scanner.scan_tokens()

        print(list(map(str, tokens)))

        parser = Parser(tokens, self.error_token)
        expr = parser.parse()

        if Lox.has_error:
            print('has error')
            return

        print(expr)
        print(AstPrinter().print(expr))

    def run_file(self, path):
        with open(path, 'r') as file:
            code_lines = file.readlines()

        code = '\n'.join(code_lines)
        self.run_code(code)

        if self.has_error:
            exit(65)

    def run_prompt(self, ):
        while True:
            self.run_code(input('>'))
            self.has_error = False

    def run(self):
        if len(sys.argv) > 2:
            print("Usage: pylox [script]")
            exit(64)
        elif len(sys.argv) == 2:
            self.run_file(sys.argv[1])
        else:
            self.run_prompt()

    @staticmethod
    def error(line: int, message: str):
        Lox.report(line, "", message)

    @staticmethod
    def error_token(token: Token, message: str):
        if token.type == TokenType.EOF:
            Lox.report(token.line, ' at end', message)
        else:
            Lox.report(token.line, f'at "{token.lexeme}"', message)

    @staticmethod
    def report(line: int, where: str, message: str):
        print(f'[line {line}] Error{where}: {message}')
        Lox.has_error = True
