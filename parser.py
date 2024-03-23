from ops import BinOP, UnaryOP, NoOP, Assign, Var, Num, Compound
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
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_character = self.text[0]
        self.current_token = None

        self.RESERVED_KEYWORDS = {
            "BEGIN": Token(TokenType.BEGIN, "BEGIN"),
            "END": Token(TokenType.END, "END"),
        }
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

        token = self.RESERVED_KEYWORDS.get(result, Token(TokenType.ID, result))
        return token

    """
        Moves the pos marker to next position (pos+1) if possible
    """
    def advance(self):
        self.pos += 1
        if self.pos < len(self.text):
            self.current_character = self.text[self.pos]
        else:
            self.current_character = None
    
    """
        Gets continuous integer string values and returns it as an single integer
    """
    def integer(self):
        value = ""
        while self.pos < len(self.text) and self.text[self.pos].isdigit():
            value += self.text[self.pos]
            self.advance()

        return int(value)

    """
        Returns the character in next position if possible
    """
    def peek(self):
        if self.pos + 1 >= len(self.text):
            return None

        return self.text[self.pos + 1]

    """
        Parses the word and returns it as one of the allowed tokens
    """
    def get_next_token(self):
        text = self.text

        while self.current_character is not None:
            if self.pos >= len(text):
                return Token(TokenType.EOF, "")

            if self.current_character == ' ' or self.current_character == '\n':
                self.advance()
                continue

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

    """
        Gets and returns next token if given token_type is current_token type
    """
    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.current_token = self.get_next_token()
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
