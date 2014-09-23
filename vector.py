#!/usr/bin/env python

import imp
import sys

sys.path.append("src")
import Mat
import Lexer
import Parser

def printAST(ast, indent):
    print "| " * indent + str(ast[1])
    if len(ast) < 3:
        return
    for c in ast[2]:
        printAST(c, indent + 1)

if len(sys.argv) > 1:
    if sys.argv[1] in ["-h", "--help"]:
        print "Usage: ./vector.py [file.vec]"
        exit()
    try:
        stream = open(sys.argv[1]).read()
    except:
        print "No such file or directory: " + sys.argv[1]
        exit()
else:
    stream = raw_input("Vec> ")

print "Input: " + stream
lexemes = Lexer.lex(stream)
print "Lexemes: " + str(lexemes)
parser = Parser.Parser()
ast = parser.parse(lexemes)
print "AST:"
printAST(ast, 0)
