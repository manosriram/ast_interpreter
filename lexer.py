from enums import TokenType
from parser import Token

class Lexer:
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

