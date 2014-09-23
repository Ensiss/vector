class Interpreter:
    def __init__(self):
        self.scopes = []
        self.this = None
        self.pushScope()

    def eval(self, ast):
        if ast == False:
            print "Error: can't eval this expression"
            return False
        if ast[0] in ["LX_NUMBER", "LX_STRING"]:
            return ast[1]
        if ast[0] == "LX_ID":
            return self.getValue(ast[1])
        return self.call(ast[0], ast[2])

    def call(self, func, arg):
        if func[:3] != "LX_":
            print "Warning: invalid lexeme: " + func
            return
        func = "func_" + func[3:]
        try:
            method = getattr(self, func)
        except:
            print "Warning: the operator '" + func + "' is not implemented yet"
        else:
            if callable(method):
                return (method(arg))
        return 0

    def getValue(self, name):
        for scope in reversed(self.scopes):
            if name in scope:
                return scope[name]
        return None
    def setValue(self, name, value):
        for scope in reversed(self.scopes):
            if name in scope:
                scope[name] = value
                return value
        self.this[name] = value
        return value

    def pushScope(self):
        self.scopes.append({})
        self.this = self.scopes[-1]
    def popScope(self):
        self.scopes.pop()
        self.this = self.scopes[-1]

    def func_PLUS(self, c):
        return self.eval(c[0]) + self.eval(c[1])
    def func_MINUS(self, c):
        return self.eval(c[0]) - self.eval(c[1])
    def func_MULT(self, c):
        return self.eval(c[0]) * self.eval(c[1])
    def func_DIV(self, c):
        return self.eval(c[0]) / self.eval(c[1])
    def func_MODULO(self, c):
        return self.eval(c[0]) % self.eval(c[1])
    def func_POW(self, c):
        return self.eval(c[0]) ** self.eval(c[1])

    def func_ASSIGN(self, c):
        return self.setValue(c[0][1], self.eval(c[1]))
