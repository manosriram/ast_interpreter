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
    IF = 15
    ELSE = 16
    THEN = 17

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

        self.current_token = self.get_next_token()

    def error(self):
        raise Exception('Invalid syntax')
    """
        Marks the token as identifier (variable name)
    """
    def _id(self):
        result = ""
        while self.current_character is not None and (self.current_character.isalnum() or self.current_character == '_'):
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

        while self.current_character is not None:
            if self.pos >= len(text):
                return Token(TokenType.EOF, "")

            if self.current_character == ' ' or self.current_character == '\n':
                self.advance()
                continue
                #  return self.get_next_token()

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

            if self.current_character == ';':
                token = Token(TokenType.SEMI, text[self.pos])
                self.advance()
                return token

            if self.current_character == '.':
                token = Token(TokenType.DOT, text[self.pos])
                self.advance()
                return token

            if self.current_character.isalpha() or self.current_character == '_':
                return self._id()

            if self.current_character == ':' and self.peek() == '=':
                token = Token(TokenType.ASSIGN, ":=")
                self.advance()
                self.advance()
                return token
            
            self.error()

        return Token(TokenType.EOF, None)

    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.current_token = self.get_next_token()
            return self.current_token.type
        else:
            return None

    def compound_statement(self):
        self.eat(TokenType.BEGIN)
        node = self.statement_list()
        self.eat(TokenType.END)

        c = Compound()
        for n in node:
            c.children.append(n)

        return c

    def assignment_statement(self):
        left = self.variable()
        token = self.current_token
        self.eat(TokenType.ASSIGN)
        right = self.expr()
        return Assign(left=left, right=right, op=token)

    def statement(self):
        if self.current_token.type == TokenType.BEGIN:
            return self.compound_statement()
        elif self.current_token.type == TokenType.ID:
            return self.assignment_statement()
        else:
            return self.empty()

    def statement_list(self):
        node = self.statement()
        results = [node]

        while self.current_token.type == TokenType.SEMI:
            self.eat(TokenType.SEMI)
            results.append(self.statement())

        if self.current_token.type == TokenType.ID:
            return None

        return results

    def empty(self):
        return NoOP()

    def variable(self):
        v = Var(self.current_token)
        self.eat(TokenType.ID)
        return v

    def factor(self):
        token = self.current_token
        if token is None:
            return
        elif token.type == TokenType.PLUS_OPERATOR:
            t = self.current_token
            self.eat(TokenType.PLUS_OPERATOR)
            return UnaryOP(t, self.factor())
        elif token.type == TokenType.MINUS_OPERATOR:
            t = self.current_token
            self.eat(TokenType.MINUS_OPERATOR)
            return UnaryOP(t, self.factor())
        elif token.type == TokenType.INTEGER:
            self.eat(TokenType.INTEGER)
            return Num(token)
        elif token.type == TokenType.LPAREN:
            self.eat(TokenType.LPAREN)
            node = self.expr()
            self.eat(TokenType.RPAREN)
            return node
        else:
            return self.variable()

    def term(self):
        node = self.factor()
        if node is None:
            return

        while self.current_token.type in HIGH_PRECEDENCE_OPERATORS:
            operator = self.current_token
            if operator is None:
                break
            if operator.value == '*':
                self.eat(TokenType.MULTIPLY_OPERATOR)
            elif operator.value == '/':
                self.eat(TokenType.DIVIDE_OPERATOR)

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
            elif operator.value == '-':
                self.eat(TokenType.MINUS_OPERATOR)

            node = BinOP(left=node, op=operator, right=self.term())

        return node

    def program(self):
        node = self.compound_statement()
        self.eat(TokenType.DOT)
        return node

    def parse(self):
        result = self.program()
        if self.current_token.type != TokenType.EOF:
            print("syntax error")
            return None

        return result

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

    def visit_BinOP(self, node):
        if node.op.type == TokenType.PLUS_OPERATOR:
            return self.visit(node.left) + self.visit(node.right)
        if node.op.type == TokenType.MINUS_OPERATOR:
            return self.visit(node.left) - self.visit(node.right)
        if node.op.type == TokenType.MULTIPLY_OPERATOR:
            return self.visit(node.left) * self.visit(node.right)
        if node.op.type == TokenType.DIVIDE_OPERATOR:
            return self.visit(node.left) / self.visit(node.right)

    def visit_Num(self, node):
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
        name = node.value
        if self.GLOBAL_SCOPE.get(name, None):
            return self.GLOBAL_SCOPE[name]
        else:
            raise Exception(f"Variable {name} not found in scope")

    def interpret(self):
        tree = self.parser.parse()
        if tree is None:
            return ''
        
        ok = self.visit(tree)
        return ok

source = """
 BEGIN
     BEGIN
         number := 2;
         a := number + 1;
         b := 10 * a + 10 * number / 4;
         c := a - - b
     END;
     x := 11;
 END.
"""
p = Parser(source)
i = Interpreter(p)
x = i.interpret()
print(i.GLOBAL_SCOPE)
