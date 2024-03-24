from enums import TokenType

class NodeVisitor:
    def visit(self, node):
        method_name = 'visit_' + type(node).__name__
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        raise Exception('No visit_{} method'.format(type(node).__name__))


class Interpreter(NodeVisitor):
    GLOBAL_SCOPE = {}

    def __init__(self, parser):
        self.parser = parser

    def visit_UnaryOP(self, node):
        if node.op.type == TokenType.PLUS_OPERATOR:
            return +self.visit(node.expr)
        if node.op.type == TokenType.MINUS_OPERATOR:
            return -self.visit(node.expr)
        if node.op.type in [TokenType.EQUALS, TokenType.NOT_EQUALS]:
            return self.visit(node.expr)

    def visit_BinOP(self, node):
        if node.op.type == TokenType.PLUS_OPERATOR:
            return self.visit(node.left) + self.visit(node.right)
        if node.op.type == TokenType.MINUS_OPERATOR:
            return self.visit(node.left) - self.visit(node.right)
        if node.op.type == TokenType.MULTIPLY_OPERATOR:
            return self.visit(node.left) * self.visit(node.right)
        if node.op.type == TokenType.EQUALS:
            left = self.visit(node.left)
            right = self.visit(node.right)
            return left == right
        if node.op.type == TokenType.NOT_EQUALS:
            left = self.visit(node.left)
            right = self.visit(node.right)
            return left != right
        if node.op.type == TokenType.INTEGER_DIVIDE_OPERATOR:
            return self.visit(node.left) // self.visit(node.right)
        if node.op.type == TokenType.FLOAT_DIVIDE_OPERATOR:
            return float(self.visit(node.left)) / float(self.visit(node.right))

    def visit_Num(self, node):
        return node.value

    def visit_String(self, node):
        return node.value

    def visit_Equals(self, node):
        return node.value

    def visit_Compound(self, node):
        for child in node.children:
            self.visit(child)

    def visit_NoOP(self, node):
        pass

    def visit_Assign(self, node):
        v = node.left.value
        self.GLOBAL_SCOPE[v] = self.visit(node.right)

    def visit_Var(self, node):
        name = node.value.lower()
        if self.GLOBAL_SCOPE.get(name, None):
            return self.GLOBAL_SCOPE[name]
        else:
            raise Exception(f"Variable {name} not found in scope")

    def visit_Program(self, node):
        self.visit(node.block)
    
    def visit_Block(self, node):
        for d in node.declarations:
            self.visit(d)

        self.visit(node.compound_statement)

    def visit_VarDecl(self, node):
        pass

    def visit_Type(self, node):
        pass

    def interpret(self):
        tree = self.parser.parse()
        if tree is None:
            return ''
        
        ok = self.visit(tree)
        return ok
