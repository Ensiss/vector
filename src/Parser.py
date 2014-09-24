class Parser:
    def __init__(self):
        self.err = None
        self.lex = None
        self.ast = None
        self.precedence = [
            {"lx":"LX_LOR"},
            {"lx":"LX_LAND"},
            {"lx":"LX_OR"},
            {"lx":"LX_XOR"},
            {"lx":"LX_AND"},
            {"lx":["LX_EQ", "LX_NEQ"]},
            {"lx":["LX_LE", "LX_LT"]},# , "LX_GE", "LX_GT"
            {"lx":["LX_LSHIFT", "LX_RSHIFT"]},
            {"lx":["LX_PLUS", "LX_MINUS"]},
            {"lx":["LX_MULT", "LX_DIV", "LX_MODULO"]},
            {"lx":"LX_POW", "func":self.ruleUnary}];
        self.assign = ["ASSIGN", "PLUSSET", "MINUSSET", "MULTSET", "DIVSET", "MODULOSET",
                       "ANDSET", "ORSET", "XORSET", "LSHIFTSET", "RSHIFTSET"]

    def parse(self, lex):
        self.err = False
        self.lex = lex
        self.shift()
        self.ast = self.ruleAssign()
        return self.ast

    def ruleAssign(self):
        if self.lex:
            nname, nval = self.lex[0]
        if self.lex and self.accept("LX_ID") and nname[3:] in self.assign:
            node = (nname, nval, [])
            node[2].append((self.lname, self.lval))
            self.shift(); self.shift()
            tmp = self.operatorPipeline(0)
            if not tmp: return False
            node[2].append(tmp)
        else:
            node = self.operatorPipeline(0)
            if not node: return False
        return node

    def operatorPipeline(self, predId):
        state = self.precedence[predId]
        node = state["func"]() if "func" in state else self.operatorPipeline(predId + 1)

        while self.accept(state["lx"]):
            parent = (self.lname, self.lval, [node])
            self.shift()
            tmp = state["func"]() if "func" in state else self.operatorPipeline(predId + 1)
            if not tmp:
                return False
            parent[2].append(tmp)
            node = parent
        return node

    def ruleUnary(self):
        if self.accept("LX_MINUS"):
            node = (self.lname, self.lval, [])
            node[2].append(("LX_NUMBER", 0))
            self.shift()
            tmp = self.ruleBase()
            if not tmp: return False
            node[2].append(tmp)
        elif self.accept(["LX_LNOT", "LX_NOT"]):
            node = (self.lname, self.lval, [])
            self.shift()
            tmp = self.ruleBase()
            if not tmp: return False
            node[2].append(tmp)
        elif self.accept(["LX_INC", "LX_DEC"]):
            node = (self.lname, self.lval, [])
            self.shift()
            if not self.expect("LX_ID"): return False
            node[2].append((self.lname, self.lval))
            self.shift()
        else:
            if self.accept("LX_PLUS"):
                self.shift()
            node = self.ruleBase()
            if not node:
                return False
        return node

    def ruleBase(self):
        node = False
        if self.accept("LX_STRING"):
            node = (self.lname, self.lval[1:-1])
            self.shift()
        elif self.accept("LX_NUMBER"):
            node = (self.lname, float(self.lval))
            self.shift()
        elif self.accept("LX_ID"):
            node = (self.lname, self.lval)
            self.shift()
        elif self.accept("LX_LPAREN"):
            self.shift()
            node = self.ruleAssign()
            if self.expect("LX_RPAREN"):
                self.shift()
        elif self.accept("LX_LT"):
            node = ("LX_VECTOR", "<>", [])
            self.shift()
            if not self.expect("LX_NUMBER"):
                return False
            node[2].append((self.lname, int(self.lval)))
            self.shift()
            while self.accept("LX_COMMA"):
                self.shift()
                if self.expect("LX_NUMBER"):
                    node[2].append((self.lname, int(self.lval)))
                    self.shift()
            if self.expect("LX_GT"):
                self.shift()
        else:
            return False
        return node

    def accept(self, lx):
        if not self.lname:
            return False
        if type(lx) is str:
            return self.lname == lx
        elif type(lx) is list:
            return self.lname in lx
        return False

    def expect(self, lx):
        if self.accept(lx):
            return True
        err = "Expected symbol '" + lx + "'"
        if self.lname:
            err += " but got '" + self.lname + "' instead"
        self.error(err)
        return False

    def shift(self):
        while len(self.lex):
            self.lname, self.lval = self.lex.pop(0)
            if self.lval != "\n":
                break

    def error(self, msg):
        print "Error: " + msg
        self.err = True
