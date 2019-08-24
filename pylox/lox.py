from .scanner import Scanner
from .parser.parser import Parser, ParserException
from .interpreter import Interpreter, InterpreterException
from .parser.ast_printer import AstPrinter
from .token_types import TokenTypes as t
from .io import OutputStream, StdOutputStream


class Lox:

    def __init__(self, output: OutputStream=None, debug: bool=False):
        self.out = output or StdOutputStream()
        self.print_tokens = debug
        self.print_ast = debug

    def run_str(self, string: str):
        tokens = list(Scanner(string).scan_tokens())
        if self.print_tokens:
            for token in tokens:
                self._output(token)

        expression = Parser(tokens).parse()
        if self.print_ast:
            ast = AstPrinter().to_string(expression)
            self._output(ast)

        interpreter = Interpreter(self.out)
        result = interpreter.interpret(expression)
        return result

    def _output(self, data):
        self.out.send(data)


class LoxRepl:

    def __init__(self, lox: Lox):
        self.lox = lox

    def run(self):
        while True:
            line = input('> ')
            output = self.execute(line)
            print(output)

    def execute(self, input) -> str:
        try:
            output = self.lox.run_str(input)
        except ParserException as p:
            output = self._parser_exception_to_message(p)
        except InterpreterException as i:
            output = self._interpreter_exception_to_message(i)

        return str(output)

    def _parser_exception_to_message(self, exception: ParserException):
        if exception.token.type == t.EOF:
            position_msg = 'at end of file'
        else:
            position_msg = f'at token "{exception.token.lexeme}"'
        return f'{position_msg}: {exception.message}'

    def _interpreter_exception_to_message(self, exception: InterpreterException):
        expression_str = AstPrinter().to_string(exception.expression)
        return f'at expression "{expression_str}": {exception.message}'
