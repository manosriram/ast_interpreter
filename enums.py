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
    STRING = 18
