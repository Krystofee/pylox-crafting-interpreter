import sys

from scanner import Scanner


class Lox:
    has_error = False

    def run_code(self, source_code):
        scanner = Scanner(source_code, self.error)
        tokens = scanner.scan_tokens()

        for token in tokens:
            print(token)

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
    def report(line: int, where: str, message: str):
        Lox.has_error = True
        print(f'[line {line}] Error{where}: {message}')


if __name__ == '__main__':
    lox = Lox()
    lox.run()
