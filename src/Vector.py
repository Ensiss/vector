import Mat
import Lexer
from Parser import Parser
from Interpreter import Interpreter

class Vector:
    def __init__(self, debug = False):
        self.debug = debug
        self.parser = Parser()
        self.interpreter = Interpreter()

    def eval(self, s):
        if self.debug:
            print "Input: " + s
        lexemes = Lexer.lex(s)
        if self.debug:
            print "Lexemes: " + str(lexemes)
        ast = self.parser.parse(lexemes)
        if self.debug:
            print "AST:"
            self.printAST(ast, 0)
        result = self.interpreter.eval(ast)
        if self.debug:
            print "Result: ",
        print str(result)

    def printAST(self, ast, indent):
        if ast == False:
            print "| " * indent + "ERROR"
            return
        print "| " * indent + str(ast[1])
        if len(ast) < 3:
            return
        for c in ast[2]:
            self.printAST(c, indent + 1)
