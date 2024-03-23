from ops import BinOP, UnaryOP, NoOP, Assign, Var, Num, String, Compound
from enums import TokenType

class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __str__(self):
        return f"{self.type}: {self.value}"
    
    def __repr__(self):
        return f"{self.type}: {self.value}"

HIGH_PRECEDENCE_OPERATORS = [TokenType.MULTIPLY_OPERATOR, TokenType.DIVIDE_OPERATOR]
LOW_PRECEDENCE_OPERATORS = [TokenType.PLUS_OPERATOR, TokenType.MINUS_OPERATOR]

class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = None
        self.RESERVED_KEYWORDS = {
            "BEGIN": Token(TokenType.BEGIN, "BEGIN"),
            "END": Token(TokenType.END, "END"),
        }
        self.current_token = self.lexer.current_token

    """
        Gets and returns next token if given token_type is current_token type
    """
    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
            return self.current_token.type
        else:
            return None

    """
        compound_statement:
            BEGIN statement_list END
    """
    def compound_statement(self):
        self.eat(TokenType.BEGIN)
        node = self.statement_list()
        self.eat(TokenType.END)

        c = Compound()
        for n in node:
            c.children.append(n)

        return c

    """
        assignment_statement:
            ID ASSIGN expr SEMI
    """
    def assignment_statement(self):
        left = self.variable()
        token = self.current_token
        self.eat(TokenType.ASSIGN)
        right = self.expr()
        return Assign(left=left, right=right, op=token)

    """
        statement:
            compound_statement | assignment_statement | empty
    """
    def statement(self):
        if self.current_token.type == TokenType.BEGIN:
            return self.compound_statement()
        elif self.current_token.type == TokenType.ID:
            return self.assignment_statement()
        else:
            return self.empty()

    """
        statement_list:
            statement | statement SEMI statement_list
    """
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
        elif token.type == TokenType.STRING:
            self.eat(TokenType.STRING)
            return String(token)
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
            self.current_token = self.lexer.get_next_token()

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
            raise Exception("Syntax error")

        return result
