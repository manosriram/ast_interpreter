from enum import Enum

class TokenType(Enum):
    INTEGER = 1
    PLUS_OPERATOR = 2
    EOF = 3
    MINUS_OPERATOR = 4
    MULTIPLY_OPERATOR = 5
    DIVIDE_OPERATOR = 6
    LPAREN = 7
    RPAREN = 8
    
    SEMI = 9
    BEGIN = 10
    END = 11
    DOT = 12
    ASSIGN = 13
    ID = 14

HIGH_PRECEDENCE_OPERATORS = [TokenType.MULTIPLY_OPERATOR, TokenType.DIVIDE_OPERATOR]
LOW_PRECEDENCE_OPERATORS = [TokenType.PLUS_OPERATOR, TokenType.MINUS_OPERATOR]

class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __str__(self):
        return f"{self.type}: {self.value}"
    
    def __repr(self):
        return f"{self.type}: {self.value}"

RESERVED_KEYWORDS = {
    "BEGIN": Token(TokenType.BEGIN, "BEGIN"),
    "END": Token(TokenType.END, "END"),
}

class AST(object):
    pass

class NoOp(AST):
    pass

class Var(AST):
    def __init__(self, token):
        self.token = token
        self.value = self.token.value

class Compound(AST):
    def __init__(self):
        self.children = []

class AssignOP(AST):
    def __init__(self, left, op, right):
        self.left = left
        self.right = self.right
        self.token = self.op = op

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

class Num(AST):
    def __init__(self, token):
        self.token = token
        self.value = self.token.value

class Parser:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_character = self.text[0]
        self.current_token = None

    def _id(self):
        result = ""
        while self.current_character is not None and self.current_character.isalnum():
            result += self.current_character
            self.advance()

        token = RESERVED_KEYWORDS.get(result, Token(TokenType.ID, result))
        return token

    def advance(self):
        self.pos += 1
        if self.pos < len(self.text):
            self.current_character = self.text[self.pos]
        else:
            self.current_character = None
    
    def integer(self):
        value = ""
        while self.pos < len(self.text) and self.text[self.pos].isdigit():
            value += self.text[self.pos]
            self.advance()

        return int(value)

    def peek(self):
        if self.pos + 1 >= len(self.text):
            return None

        return self.text[self.pos + 1]

    def get_next_token(self):
        text = self.text

        if self.pos >= len(text):
            return Token(TokenType.EOF, "")

        if self.current_character == ' ':
            self.advance()
            return self.get_next_token()

        token = None
        if self.current_character.isdigit():
            token = Token(TokenType.INTEGER, self.integer())
            return token

        if self.current_character == '+':
            token = Token(TokenType.PLUS_OPERATOR, text[self.pos])
            self.advance()
            return token

        if self.current_character == '-':
            token = Token(TokenType.MINUS_OPERATOR, text[self.pos])
            self.advance()
            return token

        if self.current_character == '*':
            token = Token(TokenType.MULTIPLY_OPERATOR, text[self.pos])
            self.advance()
            return token

        if self.current_character == '/':
            token = Token(TokenType.DIVIDE_OPERATOR, text[self.pos])
            self.advance()
            return token

        if self.current_character == '(':
            token = Token(TokenType.LPAREN, text[self.pos])
            self.advance()
            return token

        if self.current_character == ')':
            token = Token(TokenType.RPAREN, text[self.pos])
            self.advance()
            return token

        if self.current_character.isalpha():
            return self._id()

        if self.current_character == ';':
            token = Token(TokenType.SEMI, text[self.pos])
            self.advance()
            return token

        if self.current_character == '.':
            token = Token(TokenType.DOT, text[self.pos])
            self.advance()
            return token

        if self.current_character == ':' and self.peek() == '=':
            token = Token(TokenType.ASSIGN, ":=")
            self.advance()
            self.advance()
            return token
        
        return Token(TokenType.EOF, None)

    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.current_token = self.get_next_token()
            return self.current_token.type
        else:
            return None

    def factor(self):
        token = self.current_token
        if token.type == TokenType.PLUS_OPERATOR:
            t = self.current_token
            self.eat(TokenType.PLUS_OPERATOR)
            return UnaryOP(t, self.factor())
        if token.type == TokenType.MINUS_OPERATOR:
            t = self.current_token
            self.eat(TokenType.MINUS_OPERATOR)
            return UnaryOP(t, self.factor())
        if token.type == TokenType.INTEGER:
            self.eat(TokenType.INTEGER)
            return Num(token)
        elif token.type == TokenType.LPAREN:
            self.eat(TokenType.LPAREN)
            node = self.expr()
            self.eat(TokenType.RPAREN)
            return node

    def term(self):
        node = self.factor()
        while self.current_token.type in HIGH_PRECEDENCE_OPERATORS:
            operator = self.current_token
            if operator.value == '*':
                self.eat(TokenType.MULTIPLY_OPERATOR)
                #  result *= self.factor()
            elif operator.value == '/':
                self.eat(TokenType.DIVIDE_OPERATOR)
                #  result /= self.factor()

            node = BinOP(left=node, op=operator, right=self.factor())

        return node

    def expr(self):
        if not self.current_token:
            self.current_token = self.get_next_token()

        node = self.term()

        while self.current_token.type in LOW_PRECEDENCE_OPERATORS:
            operator = self.current_token
            if operator.value == '+':
                self.eat(TokenType.PLUS_OPERATOR)
                #  result += self.term()
            elif operator.value == '-':
                self.eat(TokenType.MINUS_OPERATOR)
                #  result -= self.term()

            node = BinOP(left=node, op=operator, right=self.term())

        return node

class NodeVisitor:
    def visit(self, node):
        method_name = 'visit_' + type(node).__name__
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        raise Exception('No visit_{} method'.format(type(node).__name__))

class Interpreter(NodeVisitor):
    def __init__(self, parser):
        self.parser = parser

    def parse(self):
        return self.parser.expr()

    def visit_UnaryOP(self, node):
        if node.op.type == TokenType.PLUS_OPERATOR:
            return +self.visit(node.expr)
        if node.op.type == TokenType.MINUS_OPERATOR:
            return -self.visit(node.expr)

    def visit_BinOP(self, node):
        if node.op.type == TokenType.PLUS_OPERATOR:
            return self.visit(node.left) + self.visit(node.right)
        if node.op.type == TokenType.MINUS_OPERATOR:
            return self.visit(node.left) - self.visit(node.right)
        if node.op.type == TokenType.MULTIPLY_OPERATOR:
            return self.visit(node.left) * self.visit(node.right)
        if node.op.type == TokenType.DIVIDE_OPERATOR:
            return self.visit(node.left) * self.visit(node.right)

    def visit_Num(self, node):
        return node.value

if __name__ == "__main__":
    while True:
        inp = str(input("calc>"))
        p = Parser(inp)
        i = Interpreter(p)
        result = i.visit(i.parse())
        print(result)
