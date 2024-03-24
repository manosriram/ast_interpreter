from enum import Enum

class TokenType(Enum):
    INTEGER = 1
    REAL = 2

    PLUS_OPERATOR = 3
    EOF = 4
    MINUS_OPERATOR = 5
    MULTIPLY_OPERATOR = 6
    INTEGER_DIVIDE_OPERATOR = 7
    FLOAT_DIVIDE_OPERATOR = 8

    LPAREN = 9
    RPAREN = 10
    
    ID = 11
    VAR = 12
    SEMI = 13
    BEGIN = 14
    END = 15
    DOT = 16
    ASSIGN = 17
    IF = 18
    ELSE = 19
    STRING = 20
    EQUALS = 21
    NOT_EQUALS = 22
    PROGRAM = 23
    COMMA = 24
    COLON = 25
