from enum import Enum

class TokenType(Enum):
    INTEGER = 1
    PLUS_OPERATOR = 2
    EOF = 3
    MINUS_OPERATOR = 4
    MULTIPLY_OPERATOR = 5
    DIVIDE_OPERATOR = 6

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
            token = Token(TokenType.INTEGER, int(text[self.pos]))
            self.advance()
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

    def expr(self):
        self.current_token = self.get_next_token()
        left = str(self.current_token.value)
        
        ok = True
        while ok:
            next = self.eat(TokenType.INTEGER)
            ok = (next not in [TokenType.PLUS_OPERATOR, TokenType.MINUS_OPERATOR, TokenType.MULTIPLY_OPERATOR, TokenType.DIVIDE_OPERATOR] and next is not None)
            if ok:
                left += str(self.current_token.value)
        
        left = int(left)


        operator = self.current_token
        if operator.value == '+':
            self.eat(TokenType.PLUS_OPERATOR)
        elif operator.value == '-':
            self.eat(TokenType.MINUS_OPERATOR)
        elif operator.value == '*':
            self.eat(TokenType.MULTIPLY_OPERATOR)
        elif operator.value == '/':
            self.eat(TokenType.DIVIDE_OPERATOR)


        right = str(self.current_token.value)
        while self.eat(TokenType.INTEGER) != TokenType.EOF:
            right += str(self.current_token.value)


        right = int(right)
        if operator.value == '+':
            return left + right
        if operator.value == '-':
            return left - right
        if operator.value == '*':
            return left * right
        if operator.value == '/':
            return left / right
        else:
            print("error adding")

while True:
    inp = str(input("calc>"))
    i = Interpreter(inp)
    result = i.expr()
    print("result = ", result)
