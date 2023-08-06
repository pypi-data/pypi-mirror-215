from .parser import Parser
from .interpreter import Interpreter

class Runtime:
    def __init__(self):
        self.version = "0.2"

    def run(self, code):
        ast = self.AST(code)
        interpreter = Interpreter()
        result = interpreter.eval_program(ast)
        return result or "undefined"
    
    def AST(self, code):
        parser = Parser()
        return parser.createAST(code)