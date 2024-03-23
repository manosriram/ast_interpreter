from lexer import Lexer
from parser import Parser
from interpreter import Interpreter

source = """
 BEGIN
     BEGIN
         number := 2;
         name := 'manosriram';
         a := number + 1;
         b := 10 * a + 10 * number / 4;
         c := a - - b
     END;
     x := 11;
 END.
"""

if __name__ == "__main__":
    l = Lexer(source)
    p = Parser(l)
    i = Interpreter(p)
    x = i.interpret()
    print(i.GLOBAL_SCOPE)
