from lox.token import Token


class LoxRuntimeError(RuntimeError):
    def __init__(self, token: Token, message: str):
        self.message = message
        self.token = token
