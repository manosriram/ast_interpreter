from enum import Enum

class TokenType(Enum):
    INTEGER = 1
    PLUS_OPERATOR = 2
    EOF = 3
    MINUS_OPERATOR = 4
    MULTIPLY_OPERATOR = 5
    DIVIDE_OPERATOR = 6

HIGH_PRECEDENCE_OPERATORS = [TokenType.MULTIPLY_OPERATOR, TokenType.DIVIDE_OPERATOR]
LOW_PRECEDENCE_OPERATORS = [TokenType.PLUS_OPERATOR, TokenType.MINUS_OPERATOR]

class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __str__(self):
        return f"{self.type}: {self.value}"

class Interpreter:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_character = self.text[0]
        self.current_token = None

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

    def get_next_token(self):
        text = self.text

        if self.pos >= len(text):
            return Token(TokenType.EOF, "")

        if self.current_character == ' ':
            self.advance()
            return self.get_next_token()

        #  print(text, self.pos)
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
        
        return None

    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.current_token = self.get_next_token()
            return self.current_token.type
        else:
            return None

    def factor(self):
        token = self.current_token
        self.eat(TokenType.INTEGER)
        return token.value

    def term(self):
        result = self.factor()
        while self.current_token.type in HIGH_PRECEDENCE_OPERATORS:
            operator = self.current_token
            if operator.value == '*':
                self.eat(TokenType.MULTIPLY_OPERATOR)
                result *= self.factor()
            elif operator.value == '/':
                self.eat(TokenType.DIVIDE_OPERATOR)
                result /= self.factor()

        return result

    def expr(self):
        self.current_token = self.get_next_token()
        result = self.term()

        while self.current_token.type in LOW_PRECEDENCE_OPERATORS:
            operator = self.current_token
            if operator.value == '+':
                self.eat(TokenType.PLUS_OPERATOR)
                result += self.term()
            elif operator.value == '-':
                self.eat(TokenType.MINUS_OPERATOR)
                result -= self.term()

        return result

while True:
    inp = str(input("calc>"))
    i = Interpreter(inp)
    result = i.expr()
    print("result = ", result)
