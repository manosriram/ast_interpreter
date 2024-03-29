class AST(object):
    pass

class UnaryOP(AST):
    def __init__(self, op, expr):
        self.token = self.op = op
        self.expr = expr

class BinOP(AST):
    def __init__(self, left, right, op):
        self.left = left
        self.right = right
        self.token = self.op = op

    def p(self):
        if type(self) == BinOP:
            #  print(self.token)
            if type(self.left) == BinOP:
                self.left.p()
                print(self.left.token)
            else:
                print(self.left.type, self.left.value)
            if type(self.right) == BinOP:
                self.right.p()
                print(self.left.token)
            else:
                print(self.right.type, self.right.value)
        else:
            print(self.value)
            return

class NoOP(AST):
    pass

class Var(AST):
    def __init__(self, token):
        self.token = token
        self.value = self.token.value

class Compound(AST):
    def __init__(self):
        self.children = []

class Assign(AST):
    def __init__(self, left, op, right):
        self.left = left
        self.right = right
        self.token = self.op = op

class Num(AST):
    def __init__(self, token):
        self.token = token
        self.value = self.token.value

class String(AST):
    def __init__(self, token):
        self.token = token
        self.value = self.token.value

class Block(AST):
    def __init__(self, declarations, compound_statement):
        self.declarations = declarations
        self.compound_statement = compound_statement

class VarDecl(AST):
    def __init__(self, var_node, type_node):
        self.var_node = var_node
        self.type_node = type_node

class Program(AST):
    def __init__(self, name, block):
        self.name = name
        self.block = block

class Type(AST):
    def __init__(self, token):
        self.token = token
        self.value = self.token.value

