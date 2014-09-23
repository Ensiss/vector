import re

lexlist = [
    # Keywords
    ("LX_IF", 'if(?![a-zA-Z0-9_])'),
    ("LX_ELSE", 'else(?![a-zA-Z0-9_])'),
    ("LX_WHILE", 'while(?![a-zA-Z0-9_])'),
    ("LX_DO", 'do(?![a-zA-Z0-9_])'),
    ("LX_FOR", 'for(?![a-zA-Z0-9_])'),
    ("LX_FUNC", 'function(?![a-zA-Z0-9_])'),
    ("LX_VAR", 'var(?![a-zA-Z0-9_])'),
    ("LX_RETURN", 'return(?![a-zA-Z0-9_])'),

    # Constants
    ("LX_ID", '[a-zA-Z_][a-zA-Z0-9_]*'),
    ("LX_NUMBER", '[0-9]+(\\.[0-9]*)?'),
    ("LX_STRING", '"(\\\\"|[^"])*"|' + "'(\\\\'|[^'])*'"),

    # Punctuation
    ("LX_LPAREN", '\\('),
    ("LX_RPAREN", '\\)'),
    ("LX_LCURLY", '\\{'),
    ("LX_RCURLY", '\\}'),
    ("LX_LBRACKET", '\\['),
    ("LX_RBRACKET", '\\]'),
    ("LX_SEMICOLON", ';'),
    ("LX_COLON", ':'),
    ("LX_COMMA", ','),
    ("LX_DOT", '\\.'),

    # Logical
    ("LX_LAND", '&&'),
    ("LX_LOR", '\\|\\|'),

    # Special assign
    ("LX_PLUSSET", '\\+='),
    ("LX_MINUSSET", '-='),
    ("LX_MULTSET", '\\*='),
    ("LX_DIVSET", '/='),
    ("LX_MODULOSET", '%='),
    ("LX_ANDSET", '&='),
    ("LX_ORSET", '\\|='),
    ("LX_XORSET", '\\^='),
    ("LX_LSHIFTSET", '<<='),
    ("LX_RSHIFTSET", '>>='),

    # Binary
    ("LX_AND", '&'),
    ("LX_OR", '\\|'),
    ("LX_XOR", '\\^'),
    ("LX_NOT", '~'),
    ("LX_LSHIFT", '<<'),
    ("LX_RSHIFT", '>>'),

    # Comparison
    ("LX_EQ", '=='),
    ("LX_NEQ", '!='),
    ("LX_LE", '<='),
    ("LX_GE", '>='),
    ("LX_LT", '<'),
    ("LX_GT", '>'),

    # Logical not
    ("LX_LNOT", '!'),

    # Assignment
    ("LX_ASSIGN", '='),

    # Operators
    ("LX_INC", '\\+\\+'),
    ("LX_DEC", '--'),
    ("LX_POW", '\\*\\*'),
    ("LX_PLUS", '\\+'),
    ("LX_MINUS", '-'),
    ("LX_MULT", '\\*'),
    ("LX_DIV", '/'),
    ("LX_MODULO", '%')
]

def lex(s):
    lexemes = []
    while s:
        match = re.search("^[ \t\v\f]+", s)
        if not match:
            match = re.search("^[\r\n]+", s)
            if match:
                lexemes.append(("LX_NEWLINE", "\n"))
        if not match:
            for name, rx in lexlist:
                match = re.search("^(" + rx + ")", s)
                if match:
                    lexemes.append((name, match.group(0)))
                    break
        if match:
            s = s[len(match.group(0)):]
        else:
            match = re.search("^\S+", s)
            if match:
                print "Unknown lexeme: " + match.group(0)
                s = s[len(match.group(0)):]
        if not match:
            break
    return lexemes
