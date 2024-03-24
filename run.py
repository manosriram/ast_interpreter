from lexer import Lexer
from parser import Parser
from interpreter import Interpreter

source = """
 begin
     BEGIN
         number := 2;
         name := 'manosriram';
         a := NUMBER + 1;
         b := 10 * a + 10 * number / 4;
         z := (1+2-2) == (10-9);
         y := 'mano' != 'mano';
         c := a - - b
     END;
     x := 11;
 end.
"""

if __name__ == "__main__":
    l = Lexer(source)
    p = Parser(l)
    i = Interpreter(p)
    x = i.interpret()
    print(i.GLOBAL_SCOPE)
    """
        {'number': 2, 'name': 'manosriram', 'a': 3, 'b': 35.0, 'z': True, 'y': False, 'c': 38.0, 'x': 11}
    """
